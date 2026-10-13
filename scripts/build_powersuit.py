#!/usr/bin/env python3
"""The CTO powersuit pages, from the powersuit repository at the release pinned in site/powersuit.yml.

    python3 scripts/build_powersuit.py               clone the pinned release into a temporary folder, then build
    python3 scripts/build_powersuit.py --repo DIR    read from an existing clone of the powersuit repository
    python3 scripts/build_powersuit.py --check       write nothing; exit 1 when a page, a block or a list differs

Every file is read from the pinned commit with git (git show), never from a working tree, and the build stops when the
tag resolves to another commit or the manifest's plugins differ from site/powersuit.yml.

Writes:
- cto-powersuit/<plugin>/index.html for each plugin: its line from site/powersuit.yml, the version, the skills (the
  command and the first sentence of each description), the gate checks, the README introduction, the install commands
  pinned to the release, and links to the source at the release;
- cto-powersuit/modules.json: the areas and the plugin pages, which scripts/site_chrome.py reads for the navigation
  tree, the powersuit sidebar and the structured data of each plugin page;
- the static blocks powersuit-eyebrow, powersuit-install, powersuit-latest, powersuit-areas, powersuit-knowledge and
  powersuit-release on /cto-powersuit/;
- the sitemap block powersuit and the llms.txt section "CTO powersuit plugins";
then the chrome of every page it wrote. A plugin page's lastmod moves to today only when its content changes.
Every release name on the overview comes from its static blocks; the build stops when the hand-written text names one.
Stdlib and git only. Tests of the parsers: python3 scripts/test_build_powersuit.py.
"""
import atexit, datetime, html, json, posixpath, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import inside_chrome, mini_yaml, site_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://machinebehavior.io'
CFG_FILE = ROOT / 'site' / 'powersuit.yml'
OUT = ROOT / 'cto-powersuit'
OVERVIEW = OUT / 'index.html'
MODULES_JSON = OUT / 'modules.json'
TODAY = datetime.date.today().isoformat()
STOP = re.compile(r'\s(?:Use when|Use it when|Use before|Use after|Use on|Use to|Use once|Activates on)\b')


def fail(msg):
    print('build_powersuit: ' + msg, file=sys.stderr)
    sys.exit(2)


def esc(s):
    return html.escape(str(s), quote=True)


class Repo:
    """Reads files of one commit with git, so nothing in a working tree can change what the pages say."""

    def __init__(self, path, commit):
        self.path, self.commit = path, commit

    def git(self, *args):
        r = subprocess.run(['git', '-C', str(self.path), *args], capture_output=True, text=True)
        if r.returncode:
            fail(f'git {" ".join(args)}: {r.stderr.strip()}')
        return r.stdout

    def read(self, rel):
        return self.git('show', f'{self.commit}:{rel}')

    def files(self, rel):
        return self.git('ls-tree', '-r', '--name-only', self.commit, rel).split()


def open_repo(cfg, path):
    src = cfg['source']
    if path is None:
        tmp = tempfile.mkdtemp(prefix='powersuit-')
        atexit.register(shutil.rmtree, tmp, True)
        r = subprocess.run(['git', 'clone', '--quiet', '--depth', '1', '--branch', src['ref'], src['repo'] + '.git', tmp],
                           capture_output=True, text=True)
        if r.returncode:
            fail(f'clone of {src["repo"]} at {src["ref"]} failed: {r.stderr.strip()}')
        path = tmp
    repo = Repo(path, src['commit'])
    got = repo.git('rev-parse', f'{src["ref"]}^{{commit}}').strip()
    if got != src['commit']:
        fail(f'{src["ref"]} is {got} in {path}, not {src["commit"]} as site/powersuit.yml pins it')
    return repo


# ---------- Markdown, the small part READMEs and skill descriptions use ----------
def inline(s, link):
    """Inline Markdown to HTML: code spans, bold, links. link(target) returns the href for a link target."""
    parts = re.split(r'(`[^`]+`)', s)
    out = ''
    for p in parts:
        if p.startswith('`') and p.endswith('`') and len(p) > 1:
            out += f'<code>{esc(p[1:-1])}</code>'
            continue
        p = esc(p).replace('&#x27;', "'")
        p = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)
        out += p
    # links last, over the escaped text; a link text may hold a code span
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{esc(link(html.unescape(m.group(2))))}">{m.group(1)}</a>', out)


def block(md, link):
    """Paragraphs and pipe tables."""
    out = []
    for para in re.split(r'\n\s*\n', md.strip()):
        lines = para.strip().splitlines()
        if lines and lines[0].startswith('|') and len(lines) > 1 and re.match(r'^\|[\s:|-]+\|$', lines[1].strip()):
            cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]  # noqa: E731
            head = ''.join(f'<th>{inline(c, link)}</th>' for c in cells(lines[0]))
            rows = ''.join('<tr>' + ''.join(f'<td>{inline(c, link)}</td>' for c in cells(l)) + '</tr>' for l in lines[2:])
            out.append(f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        else:
            out.append(f'<p class="thesis">{inline(" ".join(l.strip() for l in lines), link)}</p>')
    return '\n'.join(out)


def first_sentence(s):
    s = STOP.split(s)[0].strip()
    m = re.match(r'(.+?[.!?])(?:\s+[A-Z(`"]|$)', s)
    return m.group(1) if m else s


# ---------- the repository data ----------
def front_matter(text):
    m = re.match(r'---\n(.*?)\n---', text, re.S)
    if not m:
        return {}
    fm = m.group(1)
    name = re.search(r'^name:\s*(.+)$', fm, re.M)
    d = re.search(r'^description:[ \t]*[>|]-?[ \t]*\n((?:[ \t]+.*\n?)+)', fm, re.M) or re.search(r'^description:[ \t]*(.+)$', fm, re.M)
    inv = re.search(r'^user-invocable:\s*(\w+)', fm, re.M)
    desc = ' '.join(x.strip() for x in d.group(1).splitlines()).strip().strip('"') if d else ''
    return {'name': name.group(1).strip() if name else '', 'description': desc,
            'invocable': (inv.group(1) != 'false') if inv else True}


def readme_intro(text):
    """The paragraphs after the title, up to the install line, a demo line, a code block or the first heading."""
    body = text.split('\n', 1)[1] if '\n' in text else ''
    keep = []
    for para in re.split(r'\n\s*\n', body):
        p = para.strip()
        if not p:
            continue
        if re.match(r'(Install\b|Demo:|#|```)', p):
            break
        keep.append(p)
    return '\n\n'.join(keep)


def definition():
    """The definition of the term, from the overview's entry in site/nav.yml: one copy for every page that carries it."""
    def walk(items):
        for it in items or []:
            if it.get('url') == '/cto-powersuit/':
                return it
            hit = walk(it.get('pages'))
            if hit:
                return hit
    nav = mini_yaml.load_file(ROOT / 'site' / 'nav.yml')
    entry = walk([p for s in nav['sections'] for p in (s.get('pages') or [])])
    if not entry or not (entry.get('software') or {}).get('description'):
        fail('site/nav.yml: no software.description on the /cto-powersuit/ entry')
    return entry['software']['description']


def load(cfg, repo):
    ref = cfg['source']['ref']
    manifest = json.loads(repo.read('.claude-plugin/marketplace.json'))
    version = manifest.get('metadata', {}).get('version')
    if 'v' + str(version) != ref:
        fail(f'the manifest at {ref} says version {version}')
    listed = [m['name'] for a in cfg['areas'] for m in a['modules']] + [m['name'] for m in cfg['knowledge']['modules']]
    names = [p['name'] for p in manifest['plugins']]
    if sorted(listed) != sorted(names) or len(set(listed)) != len(listed):
        fail(f'site/powersuit.yml lists {sorted(listed)}, the manifest at {ref} lists {sorted(names)}')
    changelog = repo.read('CHANGELOG.md')
    m = re.search(rf'^## \[{re.escape(str(version))}\] - (\d{{4}}-\d{{2}}-\d{{2}})', changelog, re.M)
    if not m:
        fail(f'CHANGELOG.md at {ref} has no entry for {version}')
    release = {'ref': ref, 'commit': cfg['source']['commit'], 'version': str(version), 'date': m.group(1),
               'repo': cfg['source']['repo'], 'slug': cfg['source']['repo'].split('github.com/', 1)[-1], 'plugins': len(names),
               'definition': definition()}
    data = {}
    for p in manifest['plugins']:
        n = p['name']
        base = f'plugins/{n}'
        files = repo.files(base)
        pj = json.loads(repo.read(f'{base}/.claude-plugin/plugin.json'))
        skills = []
        for f in sorted(f for f in files if re.fullmatch(rf'{base}/skills/[^/]+/SKILL\.md', f)):
            fm = front_matter(repo.read(f))
            if not fm.get('name'):
                fail(f'{f} has no name in its front matter')
            skills.append({'name': fm['name'], 'invocable': fm['invocable'], 'line': first_sentence(fm['description']), 'path': f})
        checks = []
        for f in sorted(f for f in files if re.fullmatch(rf'{base}/checks/[^/]+\.py', f)):
            cm = re.search(r'^ID\s*=\s*"([^"]+)"', repo.read(f), re.M)
            if not cm:
                fail(f'{f} has no ID line')
            cid = cm.group(1)
            for kind in ('pass', 'fail'):  # the pages say each check has both fixtures
                if not any(x.startswith(f'{base}/checks/fixtures/{cid}/{kind}/') for x in files):
                    fail(f'{cid} has no {kind} fixture under {base}/checks/fixtures/{cid}/{kind}/')
            checks.append(cid)
        data[n] = {'version': pj.get('version'), 'license': pj.get('license'), 'skills': skills, 'checks': checks,
                   'intro': readme_intro(repo.read(f'{base}/README.md'))}
    return release, data


# ---------- pages ----------
def order(cfg):
    out = []
    for a in cfg['areas']:
        out += [(a, m) for m in a['modules']]
    k = cfg['knowledge']
    return out + [(k, m) for m in k['modules']]


def demo_html(m, cls=''):
    if not m.get('demo_url'):
        return '<span class="ps-none">No public page yet</span>'
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{esc(m["demo_url"])}">{esc(m["demo_title"])}</a>'


def line_html(m):
    return inline(m['line'], lambda u: u)


def link_for(release, n):
    """Resolve a link in plugins/<n>/README.md: a sibling plugin goes to its page here, anything else to GitHub at the release."""
    def link(target):
        if re.match(r'(https?:|mailto:)', target):
            return target
        path, _, frag = target.partition('#')
        if not path:
            return f'{release["repo"]}/blob/{release["ref"]}/plugins/{n}/README.md#{frag}'
        full = posixpath.normpath(posixpath.join(f'plugins/{n}', path))
        sib = re.fullmatch(r'plugins/([a-z0-9-]+)', full)
        if sib:
            return f'/cto-powersuit/{sib.group(1)}/'
        kind = 'tree' if path.endswith('/') or '.' not in posixpath.basename(full) else 'blob'
        return f'{release["repo"]}/{kind}/{release["ref"]}/{full}' + (f'#{frag}' if frag else '')
    return link


def plugin_page(cfg, release, data, i, seq):
    area, m = seq[i]
    n, d = m['name'], data[m['name']]
    prev_n = seq[i - 1][1]['name'] if i else None
    next_n = seq[i + 1][1]['name'] if i + 1 < len(seq) else None
    sk, ck = len(d['skills']), len(d['checks'])
    plain_line = re.sub(r'`([^`]+)`', r'\1', m['line'])
    desc = (f'{n}, a plugin of the CTO powersuit by Stefan Coetzee for Claude Code: {plain_line} '
            f'Version {d["version"]} in release {release["ref"]}, {sk} skills, {ck} gate check{"s" if ck != 1 else ""}.')
    skills = ''.join(
        f'<li class="ps-skill"><code class="ps-cmd">{esc(("/" + n + ":" + s["name"]) if s["invocable"] else s["name"])}</code>'
        f'<p>{inline(s["line"], lambda u: u)}</p></li>' for s in d['skills'])
    checks = (''.join(f'<li><code>{esc(c)}</code></li>' for c in d['checks']) if d['checks'] else '')
    checks_html = (f'<p class="thesis">The checks this plugin adds to the deploy gate of the <a href="/cto-powersuit/gate/"><code>gate</code></a> module, each with a pass fixture and a fail fixture:</p>'
                   f'<ul class="ps-checks">{checks}</ul>') if d['checks'] else '<p class="thesis">This plugin has no gate check.</p>'
    src = f'{release["repo"]}/tree/{release["ref"]}/plugins/{n}'
    pager = ('<nav class="ps-pager" aria-label="More plugins">'
             + (f'<a href="/cto-powersuit/{prev_n}/" rel="prev"><span>Previous</span><code>{prev_n}</code></a>' if prev_n else '<span></span>')
             + (f'<a href="/cto-powersuit/{next_n}/" rel="next"><span>Next</span><code>{next_n}</code></a>' if next_n else '<span></span>')
             + '</nav>')
    title = f'{n}: a CTO powersuit plugin'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}: Machine Behavior</title>
<meta name="description" content="{esc(desc)}">
<meta name="mb-source" content="site/powersuit.yml">
<link rel="canonical" href="{BASE}/cto-powersuit/{n}/">
<link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/cto-powersuit/powersuit.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛋️</text></svg>">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/cto-powersuit/{n}/">
<meta property="og:site_name" content="Machine Behavior">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(plain_line)}">
<meta name="twitter:card" content="summary">
<meta property="article:published_time" content="{cfg["published"]}">
</head>
<body class="ps-page">
<div class="sheet" id="main" role="main">

  <header class="ps-hero">
    <div class="eyebrow">{esc(area["title"])} · CTO powersuit · release {release["ref"]}, {release["date"]}</div>
    <h1 class="ps-name">{esc(n)}</h1>
    <p class="subtitle">{esc(area["about"])}</p>
  </header>

<p class="thesis ps-line">{line_html(m)}</p>
<ul class="ps-facts">
<li>Version <strong>{esc(d["version"])}</strong></li>
<li><strong>{sk}</strong> skill{"s" if sk != 1 else ""}</li>
<li><strong>{ck}</strong> gate check{"s" if ck != 1 else ""}</li>
<li>Running on this site: {demo_html(m)}</li>
</ul>

<h2 id="what-it-does">What it does</h2>
{block(d["intro"], link_for(release, n))}

<h2 id="install">Install</h2>
<p class="thesis">Add the marketplace at release {release["ref"]} once, then install the plugin and restart Claude Code.</p>
<pre><code>claude plugin marketplace add {release["slug"]}#{release["ref"]}
claude plugin install {n}@cto-powersuit</code></pre>

<h2 id="skills">Skills</h2>
<ul class="ps-skills">{skills}</ul>

<h2 id="gate-checks">Gate checks</h2>
{checks_html}

<h2 id="source">Source</h2>
<p class="thesis">{esc(release["definition"]).replace("&#x27;", "'")} <code>{esc(n)}</code> is one of its {release["plugins"]} plugins, published by Stefan Coetzee.</p>
<p class="thesis">The skills, templates, checks, fixtures, and the full README of <code>{esc(n)}</code> at release {release["ref"]}: <a href="{src}">github.com/{release["slug"]}/tree/{release["ref"]}/plugins/{n}</a>. License: {esc(d["license"] or "MIT")}. Every plugin of the powersuit: <a href="/cto-powersuit/">CTO powersuit</a>.</p>

{pager}

  <div class="footer">
    <span class="sig">Stefan Coetzee, 2026</span>
    <span class="motto">The receipts are the argument.</span>
  </div>
</div>
</body>
</html>
'''


def tiles(cfg, mods, kb=False):
    out = ''
    for m in mods:
        cls = 'ps-tile ps-tile-kb' if kb else 'ps-tile'
        out += (f'<li class="{cls}"><a class="ps-tile-name" href="/cto-powersuit/{m["name"]}/"><code>{esc(m["name"])}</code></a>'
                f'<p class="ps-tile-line">{line_html(m)}</p>'
                f'<p class="ps-tile-demo"><span class="ps-label">Running on this site</span>{demo_html(m, "ps-arrow")}</p></li>')
    return out


def areas_block(cfg):
    rows = ''
    for a in cfg['areas']:
        rows += (f'<div class="ps-area"><div class="ps-area-head"><h3>{esc(a["title"])}</h3><p>{esc(a["about"])}</p></div>'
                 f'<ol class="ps-tiles">{tiles(cfg, a["modules"])}</ol></div>')
    return f'<div class="ps-areas">{rows}</div>'


def knowledge_block(cfg):
    return f'<ol class="ps-tiles ps-tiles-kb" aria-label="Knowledge infrastructure plugins">{tiles(cfg, cfg["knowledge"]["modules"], True)}</ol>'


def install_block(release):
    r, d, repo = release['ref'], release['date'], release['repo']
    return (f'<p class="thesis">The latest release is {r}, tagged on {d}. The commands below pin it. The repository is the only source of the project: '
            f'install it only with these owner-qualified commands or from a clone of the repository.</p>\n'
            f'<pre><code>claude plugin marketplace add {release["slug"]}#{r}\nclaude plugin install sdlc@cto-powersuit</code></pre>\n'
            f'<p class="thesis">Install each plugin you need by its name from the tiles below, as <code>&lt;plugin&gt;@cto-powersuit</code>, and restart Claude Code after installing. '
            f'Inside Claude Code the same commands work as <code>/plugin marketplace add</code> and <code>/plugin install</code>. With the skills CLI:</p>\n'
            f'<pre><code>npx skills add {release["slug"]}#{r}</code></pre>\n'
            f'<p class="thesis">The skills CLI copies the skill folders only. Skills that copy templates, the hooks, and the MCP server need the plugin install. '
            f'Without <code>#{r}</code>, both installers follow the main branch. On an existing repository, start with <code>/sdlc:sdlc-audit</code>: '
            f'it needs no other module and names the module that fills each gap. To move a pin or roll back, see '
            f'<a href="{repo}/blob/{r}/README.md#versions-and-rollback">Versions and rollback</a> in the README at {r}.</p>')


def eyebrow_block(release):
    return f'Open source · MIT license · latest release {release["ref"]}, {release["date"]}'


def latest_block(release):
    r, repo = release['ref'], release['repo']
    first = 'v0.1.0' if r == 'v0.1.0' else 'The first release, v0.1.0,'
    return (f'<strong>Latest release:</strong> <a href="{repo}/releases/tag/{r}">{r}</a>, {release["date"]}. '
            f'Every release after v0.1.0 carries a source tarball of its tag, the tarball\'s sha256, and a build provenance attestation. '
            f'{first} was tagged before the release workflow existed and has neither.')


def release_block(release, data, note=None):
    sk = sum(len(d['skills']) for d in data.values())
    ck = sum(len(d['checks']) for d in data.values())
    return (f'<p class="thesis">The plugin list, the lines, and the plugin pages follow release <a href="{release["repo"]}/releases/tag/{release["ref"]}">{release["ref"]}</a> '
            f'of {release["date"]}: {release["plugins"]} plugins with {sk} skills and {ck} gate checks. Each plugin page links its source at that release. '
            f'Changes on the main branch since the release are in the changelog under Unreleased.'
            + (f' {inline(note, lambda u: u)}' if note else '') + '</p>')


def sections(src):
    return [{'id': i, 'title': html.unescape(re.sub(r'<[^>]+>', '', t)).strip()}
            for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', src, re.S)]


def modules_json(cfg, release, data, overview_src):
    def entry(m):
        return {'name': m['name'], 'url': f'/cto-powersuit/{m["name"]}/'}
    pages = []
    for area, m in order(cfg):
        n = m['name']
        pages.append({'title': n, 'url': f'/cto-powersuit/{n}/', 'software': {
            'name': f'{n} (CTO powersuit plugin)', 'alternate_name': f'{n}@cto-powersuit',
            'description': re.sub(r'`([^`]+)`', r'\1', m['line']),
            'repository': release['repo'], 'license': f'{release["repo"]}/blob/{release["ref"]}/LICENSE',
            'version': data[n]['version'], 'platform': 'Claude Code', 'part_of': '/cto-powersuit/#software'}})
    groups = [{'title': a['title'], 'modules': [entry(m) for m in a['modules']]} for a in cfg['areas']]
    k = cfg['knowledge']
    return {'generated_by': 'scripts/build_powersuit.py', 'release': release,
            'sections': sections(overview_src), 'areas': groups,
            'knowledge': {'title': k['title'], 'modules': [entry(m) for m in k['modules']]}, 'pages': pages}


def put_static(src, name, body):
    rx = re.compile(rf'<!-- static:{name} -->.*?<!-- /static:{name} -->', re.S)
    if not rx.search(src):
        fail(f'cto-powersuit/index.html: no <!-- static:{name} --> block')
    return rx.sub(lambda _: f'<!-- static:{name} -->{body}<!-- /static:{name} -->', src)


def llms_body(cfg, release, data):
    out = (f'One page per plugin of the CTO powersuit at release {release["ref"]} ({release["date"]}), grouped by the area of the CTO job: '
           f'the line, the version, the skills with their commands, the gate checks, and the install commands. Overview: {BASE}/cto-powersuit/\n')
    for group in cfg['areas'] + [cfg['knowledge']]:
        out += f'\n### {group["title"]}\n\n'
        for m in group['modules']:
            d = data[m['name']]
            line = re.sub(r'`([^`]+)`', r'\1', m['line'])
            out += f'- [{m["name"]}]({BASE}/cto-powersuit/{m["name"]}/): {line} Version {d["version"]}, {len(d["skills"])} skills.\n'
    return out


def main(argv):
    check = '--check' in argv
    path = argv[argv.index('--repo') + 1] if '--repo' in argv else None
    cfg = mini_yaml.load_file(CFG_FILE)
    repo = open_repo(cfg, path)
    release, data = load(cfg, repo)
    seq = order(cfg)
    differs = []

    def write(p, text):
        old = p.read_text(encoding='utf-8') if p.exists() else None
        if old != text:
            differs.append(p.relative_to(ROOT).as_posix())
            if not check:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding='utf-8')

    # 1. the module list first: the chrome reads it for the tree, the sidebar and the structured data
    overview = OVERVIEW.read_text(encoding='utf-8')
    for name, body in (('powersuit-eyebrow', eyebrow_block(release)), ('powersuit-install', install_block(release)),
                       ('powersuit-latest', latest_block(release)), ('powersuit-areas', areas_block(cfg)),
                       ('powersuit-knowledge', knowledge_block(cfg)), ('powersuit-release', release_block(release, data, cfg['source'].get('unreleased')))):
        overview = put_static(overview, name, body)
    others = sorted(set(re.findall(r'\bv\d+\.\d+\.\d+\b', re.sub(r'<!-- (static|mb):(\S+) -->.*?<!-- /\1:\2 -->', '', overview, flags=re.S))))
    if others:  # every release name on the overview comes from the static blocks, so hand text cannot fall behind the pin
        fail(f'cto-powersuit/index.html names {", ".join(others)} outside its static blocks; move that text into a block or update it to {release["ref"]}')
    write(MODULES_JSON, json.dumps(modules_json(cfg, release, data, overview), ensure_ascii=False, indent=1) + '\n')
    if check and differs:
        print('differs:', *differs)
        return 1
    site_chrome.tree(reload=True)

    # 2. the pages, each through the chrome. A page counts as changed when it differs from the file with the chrome
    # of the current sitemap date; only then does its lastmod move to today, and the chrome runs again with that date.
    old_lastmod = dict(re.findall(r'<loc>' + re.escape(BASE) + r'(/cto-powersuit/[a-z0-9-]+/)</loc><lastmod>([0-9-]+)</lastmod>',
                                  (ROOT / 'sitemap.xml').read_text(encoding='utf-8')))
    raw, lastmod = {}, []
    for i, (area, m) in enumerate(seq):
        rel = f'cto-powersuit/{m["name"]}/index.html'
        url = f'/cto-powersuit/{m["name"]}/'
        raw[rel] = plugin_page(cfg, release, data, i, seq)
        p = ROOT / rel
        same = url in old_lastmod and p.exists() and p.read_text(encoding='utf-8') == site_chrome.apply(raw[rel], rel)
        lastmod.append((url, old_lastmod[url] if same else TODAY))
        if check and not same:
            differs.append(rel)
    if check:
        if site_chrome.apply(overview, 'cto-powersuit/index.html') != OVERVIEW.read_text(encoding='utf-8'):
            differs.append('cto-powersuit/index.html')
        if llms_body(cfg, release, data).strip() not in (ROOT / 'llms.txt').read_text(encoding='utf-8'):
            differs.append('llms.txt')
    else:
        # 3. the shared lists, then the chrome again with the new dates
        inside_chrome.sitemap_block('powersuit', lastmod, BASE, 'scripts/build_powersuit.py')
        inside_chrome.llms_section('CTO powersuit plugins', llms_body(cfg, release, data))
        site_chrome.tree(reload=True)
        for rel, page in raw.items():
            write(ROOT / rel, site_chrome.apply(page, rel))
        write(OVERVIEW, site_chrome.apply(overview, 'cto-powersuit/index.html'))
    total_sk = sum(len(d['skills']) for d in data.values())
    print(f'powersuit {release["ref"]} ({release["commit"][:12]}): {len(seq)} plugin pages, {total_sk} skills; '
          + ((f'differs: {" ".join(differs)}' if differs else 'up to date') if check else f'wrote {len(differs)} files'))
    return 1 if check and differs else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
