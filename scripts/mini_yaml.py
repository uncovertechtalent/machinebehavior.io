#!/usr/bin/env python3
"""A strict reader for the YAML subset used by services/*.yml and incidents/*.yml. Stdlib only.

Supported: mappings and lists by indentation (spaces only), '- ' list items holding scalars or mappings,
flow lists '[a, b]', quoted and plain scalars, integers, true/false, null/~, folded '>' and literal '|'
block scalars, and '#' comments. Anything else raises YamlError with the file and line, so a typo stops
the build instead of producing a wrong page.
"""
import re


class YamlError(ValueError):
    pass


def _scalar(s, where):
    s = s.strip()
    if s == '' or s in ('~', 'null'):
        return None
    if s in ('true', 'false'):
        return s == 'true'
    if re.fullmatch(r'-?\d+', s):
        return int(s)
    if s[0] in '"\'':
        q = s[0]
        if len(s) < 2 or s[-1] != q:
            raise YamlError(f'{where}: unclosed quote')
        body = s[1:-1]
        return body.replace("''", "'") if q == "'" else body.encode('utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
    if s[0] == '[':
        if s[-1] != ']':
            raise YamlError(f'{where}: unclosed flow list')
        inner = s[1:-1].strip()
        return [_scalar(x, where) for x in _split_flow(inner, where)] if inner else []
    if s[0] in '{&*!|>@`':
        raise YamlError(f'{where}: unsupported syntax {s[:20]!r}')
    if ': ' in s or s.endswith(':'):
        raise YamlError(f'{where}: a plain value may not contain ": " (quote it)')
    return s


def _split_flow(s, where):
    out, cur, q = [], '', None
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch; cur += ch
        elif ch == ',':
            out.append(cur); cur = ''
        elif ch in '[]{}':
            raise YamlError(f'{where}: nested flow collections are not supported')
        else:
            cur += ch
    if q:
        raise YamlError(f'{where}: unclosed quote in flow list')
    out.append(cur)
    return [x.strip() for x in out]


def _strip_comment(line):
    q = None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in '"\'' and (i == 0 or line[i - 1] in ' [,:'):
            q = ch
        elif ch == '#' and (i == 0 or line[i - 1] == ' '):
            return line[:i].rstrip()
    return line.rstrip()


def load(text, name='<yaml>'):
    raw = text.split('\n')
    lines = []  # (lineno, indent, content, rawline)
    for n, l in enumerate(raw, 1):
        if '\t' in l[:len(l) - len(l.lstrip())]:
            raise YamlError(f'{name}:{n}: tab in indentation')
        lines.append((n, len(l) - len(l.lstrip(' ')), l.strip(), l))
    pos = 0

    def skip():
        nonlocal pos
        while pos < len(lines) and (not _strip_comment(lines[pos][3]).strip() or lines[pos][2] == '---'):
            pos += 1

    def block_scalar(indent, style, where):
        nonlocal pos
        buf, start = [], None
        while pos < len(lines):
            n, ind, content, rawl = lines[pos]
            if content and ind <= indent:
                break
            if content and start is None:
                start = ind
            buf.append(rawl[start:] if content and start is not None else '')
            pos += 1
        while buf and not buf[-1]:
            buf.pop()
        if style == '|':
            return '\n'.join(buf)
        paras, cur = [], []
        for b in buf:
            if b.strip():
                cur.append(b.strip())
            elif cur:
                paras.append(' '.join(cur)); cur = []
        if cur:
            paras.append(' '.join(cur))
        return '\n\n'.join(paras)

    def value_after(rest, indent, where):
        """rest is the text after 'key:' on the same line."""
        nonlocal pos
        rest = _strip_comment(rest).strip()
        if rest in ('>', '|', '>-', '|-'):
            return block_scalar(indent, rest[0], where)
        if rest:
            return _scalar(rest, where)
        skip()
        if pos < len(lines) and lines[pos][1] > indent:
            return parse_block(lines[pos][1])
        if pos < len(lines) and lines[pos][1] == indent and lines[pos][2].startswith('- '):
            return parse_block(indent)  # list at the same indent as its key
        return None

    def parse_block(indent):
        nonlocal pos
        skip()
        if pos >= len(lines):
            return None
        is_list = lines[pos][2].startswith('- ') or lines[pos][2] == '-'
        out = [] if is_list else {}
        while True:
            skip()
            if pos >= len(lines):
                break
            n, ind, _, rawl = lines[pos]
            content = _strip_comment(rawl).strip()
            where = f'{name}:{n}'
            if ind < indent:
                break
            if ind > indent:
                raise YamlError(f'{where}: unexpected indentation')
            if is_list:
                if not content.startswith('-'):
                    break
                item = content[1:].strip()
                pos += 1
                m = re.match(r'^([A-Za-z_][\w-]*):(?:\s+(.*))?$', item)
                if m:
                    # a mapping item: re-read this line as the first key at indent+2
                    pos -= 1
                    sub = ind + 2
                    lines[pos] = (n, sub, item, ' ' * sub + item)
                    out.append(parse_block(sub))
                else:
                    out.append(_scalar(item, where) if item else value_after('', ind, where))
            else:
                if content.startswith('- '):
                    raise YamlError(f'{where}: list item where a key was expected')
                m = re.match(r'^([A-Za-z_][\w-]*):(?:\s+(.*)|$)', content)
                if not m:
                    raise YamlError(f'{where}: expected "key: value"')
                key = m.group(1)
                if key in out:
                    raise YamlError(f'{where}: duplicate key {key}')
                pos += 1
                rest = rawl.strip()[len(key) + 1:]
                out[key] = value_after(rest, ind, where)
        return out

    skip()
    if pos >= len(lines):
        return None
    result = parse_block(lines[pos][1])
    skip()
    if pos < len(lines):
        raise YamlError(f'{name}:{lines[pos][0]}: could not parse')
    return result


def load_file(path):
    from pathlib import Path
    p = Path(path)
    return load(p.read_text(encoding='utf-8'), str(p))


if __name__ == '__main__':
    import json, sys
    for f in sys.argv[1:]:
        print(json.dumps(load_file(f), indent=1, ensure_ascii=False))
