#!/usr/bin/env python3
"""Tests for the parsers in scripts/build_powersuit.py, on strings shaped like the powersuit repository's files: the
first sentence of a skill description, SKILL.md front matter, the README introduction, links in a README, and the
inline and table Markdown. Stdlib only; no network and no repository needed.

    python3 scripts/test_build_powersuit.py

Exits 1 when a case fails.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repository
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_powersuit as bp  # noqa: E402

REL = {'repo': 'https://github.com/o/r', 'ref': 'v9.9.9'}


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

    # links in plugins/<n>/README.md
    link = bp.link_for(REL, 'ai-ops')
    case('link: sibling plugin goes to its page here', link('../vestige/'), '/cto-powersuit/vestige/')
    case('link: file in the plugin goes to GitHub at the release', link('skills/metering/SKILL.md'),
         'https://github.com/o/r/blob/v9.9.9/plugins/ai-ops/skills/metering/SKILL.md')
    case('link: folder goes to a tree URL', link('templates/'), 'https://github.com/o/r/tree/v9.9.9/plugins/ai-ops/templates')
    case('link: anchor in the README', link('#install'), 'https://github.com/o/r/blob/v9.9.9/plugins/ai-ops/README.md#install')
    case('link: absolute stays', link('https://example.test/x'), 'https://example.test/x')

    # inline Markdown and tables
    case('inline: code, bold, link with code, escaping',
         bp.inline('Use `a<b>` and **this** with [`vestige`](../vestige/) & more', link),
         'Use <code>a&lt;b&gt;</code> and <strong>this</strong> with <a href="/cto-powersuit/vestige/"><code>vestige</code></a> &amp; more')
    case('block: table', bp.block('| A | B |\n|---|---|\n| `x` | y |', link),
         '<div class="tablewrap"><table><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td><code>x</code></td><td>y</td></tr></tbody></table></div>')

    for f in failures:
        print(f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
