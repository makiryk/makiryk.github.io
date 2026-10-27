"""Rebuild the "作ったもの" and "いま" sections of index.html from content/*.json.

Usage: python tools/build.py

Each section is replaced between its markers (<!-- works:start --> ... <!-- works:end -->,
<!-- now:start --> ... <!-- now:end -->). Everything else in index.html is left untouched.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SIZES = {"l": 52, "m": 36, "s": 32}  # icon sizes inside the 160 x 100 scene
COLORS = range(1, 9)                  # scene colour slots s1..s8 defined in style.css
CONNECTORS = {"arrow", "handoff"}     # flow items drawn as small connectors between steps
NUDGE_Y = {"robot": 2}                # icons whose drawing sits high in its box, moved down (scene units)


def icon(name, cls="ic"):
    return f'<svg class="{cls}"><use href="#i-{name}"/></svg>'


def scene(items):
    # lay the icons out side by side and centre the group in the 160 x 100 frame
    total = sum(SIZES[s] for _, s in items)
    if total > 150:
        sys.exit(f"scene is too wide ({total} > 150): use fewer or smaller icons")
    x = (160 - total) / 2
    uses = []
    for name, s in items:
        w = SIZES[s]
        y = 50 - w / 2 + NUDGE_Y.get(name, 0)
        uses.append(f'<use href="#i-{name}" x="{x:g}" y="{y:g}" width="{w}" height="{w}"/>')
        x += w
    return ('<svg class="scene" viewBox="0 0 160 100" aria-hidden="true"><rect width="160" height="100" rx="14"/>'
            + "".join(uses) + "</svg>")


def flow(steps):
    out = []
    for step in steps:
        if step in CONNECTORS:
            out.append(icon("arrow" if step == "arrow" else "handoff", "ic ar"))
        else:
            name, label = step.split(":", 1)
            out.append(f"<span>{icon(name)}{html.escape(label)}</span>")
    return '<p class="flow">' + "".join(out) + "</p>"


def work(w):
    if w["color"] not in COLORS:
        sys.exit(f'{w["name"]}: color must be 1-8')
    badge = f' <span class="badge">{html.escape(w["badge"])}</span>' if w.get("badge") else ""
    return (f'      <li class="work s{w["color"]}">\n'
            f'        {scene(w["scene"])}\n'
            f'        <div>\n'
            f'          <h3>{html.escape(w["name"])}{badge}</h3>\n'
            f'          <p class="desc">{html.escape(w["desc"])}</p>\n'
            f'          {flow(w["flow"])}\n'
            f'        </div>\n'
            f'      </li>')


def now(n):
    return (f'    <p class="now"><span class="dot" aria-hidden="true"></span>'
            f'{icon(n["icon"])}{html.escape(n["text"])}</p>')


def replace(src, key, body):
    pattern = re.compile(rf"(<!-- {key}:start -->).*?(<!-- {key}:end -->)", re.S)
    if not pattern.search(src):
        sys.exit(f"markers for '{key}' not found in index.html")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", src)


def main():
    src = INDEX.read_text(encoding="utf-8")
    known = set(re.findall(r'<symbol id="i-([\w-]+)"', src))
    works = json.loads((ROOT / "content" / "works.json").read_text(encoding="utf-8"))
    nows = json.loads((ROOT / "content" / "now.json").read_text(encoding="utf-8"))

    used = {n for w in works for n, _ in w["scene"]}
    used |= {s.split(":", 1)[0] for w in works for s in w["flow"] if s not in CONNECTORS}
    used |= {n["icon"] for n in nows}
    missing = sorted(used - known)
    if missing:
        sys.exit(f"unknown icons: {', '.join(missing)} (add a <symbol id=\"i-NAME\"> to index.html first)")

    src = replace(src, "works", "\n".join(work(w) for w in works))
    src = replace(src, "now", "\n".join(now(n) for n in nows))
    INDEX.write_text(src, encoding="utf-8", newline="\n")
    print(f"built {len(works)} works, {len(nows)} now items")


if __name__ == "__main__":
    main()
