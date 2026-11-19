"""Language card. Five Nothing modes. Forks stay out."""

import json
from pathlib import Path

from frame import dots, label, open_svg
from nothing import MODES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, data):
    colors = theme(mode)
    rows = data["languages"]
    height = 78 + len(rows) * 36 + 36
    name, _ = dots("LANGUAGES", 46, 22, colors["fg"], scale=2.1)
    parts = [
        open_svg(mode, 640, height, "Languages across public and private repositories"),
        name,
    ]
    top = rows[0][1] or 1
    for index, (lang, share) in enumerate(rows):
        y = 92 + index * 36
        bar = max(4, 280 * (share / top))
        parts.append(label(28, y, lang, colors["fg"], 15, 0.2))
        parts.append(label(168, y, f"{share:.1f}%", colors["muted"], 14, 0.3))
        parts.append(f'<rect x="250" y="{y - 12}" width="280" height="8" fill="{colors["rule"]}"/>')
        parts.append(f'<rect x="250" y="{y - 12}" width="{bar:.1f}" height="8" fill="{colors["figure"]}"/>')
    parts.append(label(28, height - 18, "Forks excluded", colors["muted"], 12, 0.8))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    data = json.loads((ROOT / "sample.json").read_text())
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for mode in MODES:
        (out / f"{mode}.svg").write_text(render(mode, data))
        print(mode)


if __name__ == "__main__":
    main()
