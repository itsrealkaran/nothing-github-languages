"""Language card. Compact is one language. Regular is the list. Wide splits them."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import languages
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    colors = theme(mode)
    if size == "compact":
        return _compact(mode, colors, data)
    if size == "wide":
        return _wide(mode, colors, data)
    return _regular(mode, colors, data)


def _compact(mode, colors, data):
    lang, share = data["languages"][0]
    name, _ = dots("LANGUAGES", 40, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} languages"),
        name,
        label(20, 100, lang, colors["figure"], 28, -0.4),
        label(340, 100, f"{share:.0f}%", colors["fg"], 28, -0.4),
        label(20, 120, f"@{data['login']}", colors["muted"], 12, 0.3),
        "</svg>",
    ])


def _regular(mode, colors, data):
    rows = data["languages"]
    height = 78 + len(rows) * 28 + 28
    name, _ = dots("LANGUAGES", 40, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, 495, height, f"{data['login']} languages"), name]
    top = rows[0][1] or 1
    for index, (lang, share) in enumerate(rows):
        y = 78 + index * 28
        bar = max(4, 250 * (share / top))
        parts.append(label(20, y, lang, colors["fg"], 13, 0.1))
        parts.append(label(150, y, f"{share:.1f}%", colors["muted"], 12, 0.2))
        parts.append(f'<rect x="220" y="{y - 10}" width="250" height="6" fill="{colors["rule"]}"/>')
        parts.append(f'<rect x="220" y="{y - 10}" width="{bar:.1f}" height="6" fill="{colors["figure"]}"/>')
    parts.append(label(20, height - 16, f"@{data['login']} · forks excluded", colors["muted"], 12, 0.4))
    parts.append("</svg>")
    return "\n".join(parts)


def _wide(mode, colors, data):
    rows = data["languages"]
    lead, share = rows[0]
    name, _ = dots("LANGUAGES", 40, 16, colors["fg"], scale=1.8)
    parts = [
        open_svg(mode, 896, 240, f"{data['login']} languages"),
        name,
        label(20, 130, f"{share:.0f}%", colors["figure"], 64, -1.5),
        label(20, 160, lead, colors["fg"], 18, 0.2),
        label(20, 188, "of the code", colors["muted"], 13, 0.4),
    ]
    rest = rows[1:] or [["—", 0]]
    top = rows[0][1] or 1
    for index, (lang, part) in enumerate(rest):
        y = 90 + index * 32
        bar = max(4, 220 * (part / top))
        parts.append(label(360, y, lang, colors["fg"], 14, 0.1))
        parts.append(label(530, y, f"{part:.1f}%", colors["muted"], 13, 0.2))
        parts.append(f'<rect x="610" y="{y - 11}" width="250" height="6" fill="{colors["rule"]}"/>')
        parts.append(f'<rect x="610" y="{y - 11}" width="{bar:.1f}" height="6" fill="{colors["figure"]}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = languages(login)
    data["login"] = login
    out = ROOT / "dist" / login
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# {login}", "", "Compact is one language. Regular is the list. Wide splits the lead language out.", ""]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += [f"### {size}", "", f"![{mode} {size}](dist/{login}/{filename})", ""]
            print(login, mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
