"""Language card for any GitHub username."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import languages
from nothing import MODES, SCALE, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    scale = SCALE[size]
    colors = theme(mode)
    rows = data["languages"]
    width = int(640 * scale)
    height = int((92 + len(rows) * 36 + 40) * scale)

    def n(value):
        return round(value * scale, 1)

    name, _ = dots("LANGUAGES", n(46), n(22), colors["fg"], scale=2.1 * scale)
    parts = [open_svg(mode, width, height, f"{data['login']} languages"), name]
    top = rows[0][1] or 1
    for index, (lang, share) in enumerate(rows):
        y = n(100 + index * 36)
        bar = max(n(4), n(280) * (share / top))
        parts.append(label(n(28), y, lang, colors["fg"], n(15), 0.2))
        parts.append(label(n(190), y, f"{share:.1f}%", colors["muted"], n(14), 0.3))
        parts.append(f'<rect x="{n(280)}" y="{y - n(12)}" width="{n(300)}" height="{n(8)}" fill="{colors["rule"]}"/>')
        parts.append(f'<rect x="{n(280)}" y="{y - n(12)}" width="{bar:.1f}" height="{n(8)}" fill="{colors["figure"]}"/>')
    parts.append(label(n(28), height - n(18), f"@{data['login']} · forks excluded", colors["muted"], n(12), 0.6))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = languages(login)
    data["login"] = login
    out = ROOT / "dist" / login
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# {login}", "", "Username, mode, and size.", ""]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += [f"### {size}", "", f"![{mode} {size}](dist/{login}/{filename})", ""]
            print(login, mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
