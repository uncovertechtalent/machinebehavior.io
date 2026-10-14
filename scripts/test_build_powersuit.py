#!/usr/bin/env python3
"""Tests for scripts/build_powersuit.py: the parsers, on strings shaped like the powersuit repository's files (the first
sentence of a skill description, SKILL.md front matter, the README introduction, links in a README, inline and table
Markdown), and the stops in load() and open_repo(), on a small repository built in a temporary folder (a moved tag, a
plugin list that differs from the manifest, a check without an ID, a check without a fail fixture). Stdlib and git;
no network.

    python3 scripts/test_build_powersuit.py

Exits 1 when a case fails.
"""
import contextlib, io, json, subprocess, sys, tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_powersuit as bp  # noqa: E402

REL = {'repo': 'https://github.com/o/r', 'ref': 'v9.9.9'}
FILES = {
    '.claude-plugin/marketplace.json': json.dumps({'name': 'mkt', 'metadata': {'version': '0.0.1'}, 'plugins': [{'name': 'a'}]}),
    'CHANGELOG.md': '# Changelog\n\n## [0.0.1] - 2026-01-02\n',
    'plugins/a/.claude-plugin/plugin.json': json.dumps({'name': 'a', 'version': '0.0.1', 'license': 'MIT'}),
    'plugins/a/README.md': '# a\n\nIntro.\n\nInstall:\n',
    'plugins/a/skills/s/SKILL.md': '---\nname: s\ndescription: Do one thing. Use when asked.\n---\n',
    'plugins/a/checks/c.py': 'ID = "a.c"\n',
    'plugins/a/checks/fixtures/a.c/pass/x.txt': 'x',
    'plugins/a/checks/fixtures/a.c/fail/x.txt': 'x',
}


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), '-c', 'user.name=test', '-c', 'user.email=test@example.test', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def commit(root, files, tag):
    for path, text in files.items():
        f = root / path
        if text is None:
            f.unlink()
        else:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text)
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', tag)
    git(root, 'tag', tag)
    return git(root, 'rev-parse', 'HEAD')


def stops(fn):
    """2 when the build stops (build_powersuit.fail), 0 when it goes through."""
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            fn()
        except SystemExit as e:
            return e.code
    return 0


def cfg(ref, commit_sha, names=('a',)):
    return {'source': {'repo': 'https://github.com/o/r', 'ref': ref, 'commit': commit_sha},
            'areas': [{'title': 'T', 'about': 'A.', 'modules': [{'name': n, 'line': 'L.'} for n in names]}],
            'knowledge': {'title': 'K', 'about': 'B.', 'modules': []}}


def main():
    failures = []

    def case(name, got, want):
        print(('ok   ' if got == want else 'FAIL ') + name)
        if got != want:
            failures.append(f'{name}: got {got!r}, want {want!r}')

    # first sentence of a description: stop before the trigger phrases, keep abbreviations and numbers inside
    case('first sentence: plain', bp.first_sentence('Write a ticket from a request. Use when a bug comes in.'), 'Write a ticket from a request.')
    case('first sentence: trigger phrase without a full stop',
         bp.first_sentence('Reference-verification gate Activates on "guess gate on".'), 'Reference-verification gate')
    case('first sentence: number with a dot', bp.first_sentence('Map controls to ISO 27001 Annex A.5 and NIS2. More text.'),
         'Map controls to ISO 27001 Annex A.5 and NIS2.')
    case('first sentence: lower-case word after a full stop stays', bp.first_sentence('Copy the vault (default ~/vault). then seed it.'),
         'Copy the vault (default ~/vault). then seed it.')

    # front matter: folded description, plain description, user-invocable
    fm = bp.front_matter('---\nname: adr\ndescription: >\n  Record one decision\n  as an ADR. Use when a decision is made.\nuser-invocable: true\n---\nbody')
    case('front matter: folded description', (fm['name'], fm['description'], fm['invocable']),
         ('adr', 'Record one decision as an ADR. Use when a decision is made.', True))
    fm = bp.front_matter('---\nname: beta\ndescription: "The untreated default."\nuser-invocable: false\n---\n')
    case('front matter: quoted one-line description, not invocable', (fm['description'], fm['invocable']), ('The untreated default.', False))
    case('front matter: missing', bp.front_matter('no front matter'), {})

    # README introduction: up to Install, Demo, a heading or a code block; tables stay
    readme = '# x\n\nFirst paragraph.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\nInstall:\n\n```bash\nclaude plugin install x\n```\n'
    case('readme intro: stops at Install', bp.readme_intro(readme), 'First paragraph.\n\n| A | B |\n|---|---|\n| 1 | 2 |')
    case('readme intro: stops at Demo', bp.readme_intro('# x\n\nOne.\n\nDemo: [a](https://a/)\n\nTwo.'), 'One.')
    case('readme intro: stops at a heading', bp.readme_intro('# x\n\nOne.\n\n## Skills\n\nTwo.'), 'One.')
    case('readme intro: a sentence with a fill-in placeholder is left out',
         bp.readme_intro('# x\n\nOne thing. Check at `<URL of the docs>`. Two things.\n\nInstall:'), 'One thing. Two things.')

    # links in plugins/<n>/README.md
    link = bp.link_for(REL, 'ai-ops')
    case('link: sibling plugin goes to its page here', link('../vestige/'), '/cto-powersuit/vestige/')
    case('link: file in the plugin goes to GitHub at the release', link('skills/metering/SKILL.md'),
         'https://github.com/o/r/blob/v9.9.9/plugins/ai-ops/skills/metering/SKILL.md')
    case('link: folder goes to a tree URL', link('templates/'), 'https://github.com/o/r/tree/v9.9.9/plugins/ai-ops/templates')
    case('link: anchor in the README', link('#install'), 'https://github.com/o/r/blob/v9.9.9/plugins/ai-ops/README.md#install')
    case('link: absolute stays', link('https://example.test/x'), 'https://example.test/x')
    case('link: a javascript: target goes to GitHub, never into an href as written', link('javascript:alert(1)'),
         'https://github.com/o/r/tree/v9.9.9/plugins/ai-ops/javascript:alert(1)')

    # inline Markdown and tables
    case('inline: code, bold, link with code, escaping',
         bp.inline('Use `a<b>` and **this** with [`vestige`](../vestige/) & more', link),
         'Use <code>a&lt;b&gt;</code> and <strong>this</strong> with <a href="/cto-powersuit/vestige/"><code>vestige</code></a> &amp; more')
    case('inline: link syntax inside a code span stays text', bp.inline('Lines like `[a](b)` and [c](../vestige/)', link),
         'Lines like <code>[a](b)</code> and <a href="/cto-powersuit/vestige/">c</a>')
    case('data link: http, mailto and root-absolute paths stay', [bp.data_link(u) for u in ('https://a/', 'mailto:a@b', '/inside/')],
         ['https://a/', 'mailto:a@b', '/inside/'])
    case('data link: a javascript: target stops the build', stops(lambda: bp.data_link('javascript:alert(1)')), 2)
    case('data link: a protocol-relative target stops the build', stops(lambda: bp.data_link('//evil.test/')), 2)
    case('demo link: a root-absolute page goes through', bp.demo_html({'name': 'x', 'demo_url': '/inside/', 'demo_title': 'Inside'}),
         '<a href="/inside/">Inside</a>')
    case('demo link: a protocol-relative target stops the build',
         stops(lambda: bp.demo_html({'name': 'x', 'demo_url': '//evil.test/', 'demo_title': 'X'})), 2)
    case('demo link: a URL without a title stops the build', stops(lambda: bp.demo_html({'name': 'x', 'demo_url': '/inside/'})), 2)
    case('block: table', bp.block('| A | B |\n|---|---|\n| `x` | y |', link),
         '<div class="tablewrap"><table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td><code>x</code></td><td>y</td></tr></tbody></table></div>')

    # the overview's hand-written text must agree with the release
    kb3 = {'knowledge': {'modules': [1, 2, 3]}}
    rel = {'plugins': 18, 'license': 'MIT'}
    case('hand text: counts and licence that agree go through',
         stops(lambda: bp.hand_text_stops(kb3, rel, '<p>18 plugins: 15 modules and 3 knowledge infrastructure plugins. The license is MIT.</p>')), 0)
    case('hand text: a release name stops the build', stops(lambda: bp.hand_text_stops(kb3, rel, '<p>Pinned to v0.2.0.</p>')), 2)
    case('hand text: a wrong count in a meta description stops the build',
         stops(lambda: bp.hand_text_stops(kb3, rel, '<meta name="description" content="19 Claude Code plugins">')), 2)
    case('hand text: another licence stops the build', stops(lambda: bp.hand_text_stops(kb3, rel, '<p>The license is Apache-2.0.</p>')), 2)
    case('hand text: a count in words stops the build when it differs',
         stops(lambda: bp.hand_text_stops(kb3, rel, '<p>Four plugins for the knowledge layer.</p>')), 2)
    case('hand text: a count in words that agrees goes through',
         stops(lambda: bp.hand_text_stops(kb3, rel, '<p>Three plugins for the knowledge layer, of eighteen plugins.</p>')), 0)
    case('hand text: British spelling and capitals count too', stops(lambda: bp.hand_text_stops(kb3, rel, '<p>Under the BSD-3-Clause Licence.</p>')), 2)
    llms = '## A\n\nx\n\n## CTO powersuit plugins\n\nbody\n- stale line\n\n## B\n\ny\n'
    case('llms section: the whole section up to the next heading, stale lines included', bp.llms_section_text(llms),
         '## CTO powersuit plugins\n\nbody\n- stale line\n')
    case('llms section: missing', bp.llms_section_text('## A\n'), None)
    case('sitemap text: one line per plugin page between the markers', bp.sitemap_text([('/cto-powersuit/a/', '2026-01-02')]),
         '  <!-- powersuit:begin (scripts/build_powersuit.py) -->\n  <url><loc>https://machinebehavior.io/cto-powersuit/a/</loc>'
         '<lastmod>2026-01-02</lastmod></url>\n  <!-- powersuit:end -->\n')
    case('hand text: static and chrome blocks are not hand text',
         stops(lambda: bp.hand_text_stops(kb3, rel, '<!-- static:x -->v0.0.1, 9 plugins<!-- /static:x --><!-- mb:head -->v0.0.2<!-- /mb:head -->')), 0)

    # the stops of load() and open_repo(), on a small repository
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        git(root, 'init', '-q')
        c1 = commit(root, FILES, 'v0.0.1')
        release, data = bp.load(cfg('v0.0.1', c1), bp.Repo(root, c1))
        case('load: release, marketplace, skills and checks',
             (release['date'], release['marketplace'], [s['name'] for s in data['a']['skills']], data['a']['checks']),
             ('2026-01-02', 'mkt', ['s'], ['a.c']))
        case('open_repo: the tag at the pinned commit goes through', stops(lambda: bp.open_repo(cfg('v0.0.1', c1), root)), 0)
        case('open_repo: a moved tag stops the build', stops(lambda: bp.open_repo(cfg('v0.0.1', '0' * 40), root)), 2)
        case('load: a plugin list that differs from the manifest stops the build',
             stops(lambda: bp.load(cfg('v0.0.1', c1, ('a', 'b')), bp.Repo(root, c1))), 2)
        c2 = commit(root, {'plugins/a/checks/fixtures/a.c/fail/x.txt': None}, 'v0.0.1-nofail')
        case('load: a check without a fail fixture stops the build', stops(lambda: bp.load(cfg('v0.0.1', c2), bp.Repo(root, c2))), 2)
        c3 = commit(root, {'plugins/a/checks/fixtures/a.c/fail/x.txt': 'x', 'plugins/a/checks/c.py': '# no id\n'}, 'v0.0.1-noid')
        case('load: a check without an ID stops the build', stops(lambda: bp.load(cfg('v0.0.1', c3), bp.Repo(root, c3))), 2)
        c4 = commit(root, {'plugins/a/checks/c.py': None, 'plugins/a/checks/fixtures/a.c/pass/x.txt': None,
                           'plugins/a/checks/fixtures/a.c/fail/x.txt': None}, 'v0.0.1-nocheck')
        case('load: a module without a gate check stops the build', stops(lambda: bp.load(cfg('v0.0.1', c4), bp.Repo(root, c4))), 2)
        c5 = commit(root, {'.claude-plugin/marketplace.json': json.dumps({'metadata': {'version': '0.0.1'}, 'plugins': [{'name': 'a'}]}),
                           'plugins/a/checks/c.py': 'ID = "a.c"\n', 'plugins/a/checks/fixtures/a.c/pass/x.txt': 'x',
                           'plugins/a/checks/fixtures/a.c/fail/x.txt': 'x'}, 'v0.0.1-noname')
        case('load: a manifest without a name stops the build', stops(lambda: bp.load(cfg('v0.0.1', c5), bp.Repo(root, c5))), 2)
        git(root, 'tag', 'v0.0.2')
        git(root, 'tag', 'v0.10.0')
        subprocess.run(['git', 'clone', '-q', '--bare', str(root), str(Path(tmp) / 'remote.git')], check=True, capture_output=True)
        case('newer tags: release tags above the pin, in version order, other tags left out',
             bp.newer_tags(str(Path(tmp) / 'remote'), 'v0.0.1'), ['v0.0.2', 'v0.10.0'])
        case('newer tags: none above the newest', bp.newer_tags(str(Path(tmp) / 'remote'), 'v0.10.0'), [])

    for f in failures:
        print(f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
