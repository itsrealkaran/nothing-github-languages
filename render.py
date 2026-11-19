"""Language card. Each language has its own share bar. Ten languages, no color key."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import languages
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    colors = theme(mode)
    rows = data["languages"][:10] or [["No languages", 0]]
    if size == "mini":
        return _lines(mode, colors, data, rows[:5], 220, 1, mark=6, margin=14)
    if size == "compact":
        return _lines(mode, colors, data, rows, 495, 2)
    if size == "wide":
        return _board(mode, colors, data, rows, 896, 5)
    return _board(mode, colors, data, rows, 495, 5)


def _pct(share):
    if share and share < 0.1:
        return f"{share:.2f}%"
    return f"{share:.1f}%"


def _share_bar(x, y, track, share, colors):
    filled = track * (share / 100) if share else 0
    if share and filled < 3:
        filled = 3
    return (
        f'<rect x="{x}" y="{y}" width="{track}" height="6" fill="{colors["rule"]}"/>'
        f'<rect x="{x}" y="{y}" width="{filled:.1f}" height="6" fill="{colors["figure"]}"/>'
    )


def _lines(mode, colors, data, rows, width, columns, mark=8, margin=20):
    """Columns of languages. The bar under each name is that language's own share."""
    rows = rows or [["No languages", 0]]
    per = (len(rows) + columns - 1) // columns
    narrow = width < 300
    gap = 16
    track = (width - margin * 2 - gap * (columns - 1)) / columns
    pitch = 34 if narrow else 38
    top = 52 if narrow else 68
    height = top + per * pitch + 8
    name, _ = dots(
        "LANGUAGES",
        margin + 14,
        12 if narrow else 16,
        colors["fg"],
        scale=1.15 if narrow else 1.8,
    )
    parts = [open_svg(mode, width, height, f"{data['login']} languages", mark=mark, margin=margin), name]
    for index, (lang, share) in enumerate(rows):
        column = index // per
        row = index % per
        x = margin + column * (track + gap)
        y = top + row * pitch
        parts.append(label(x, y, lang, colors["fg"], 12 if narrow else 13, 0.05))
        parts.append(label(x + track, y, _pct(share), colors["figure"], 12 if narrow else 13, 0.05, anchor="end"))
        parts.append(_share_bar(x, y + 8, track, share, colors))
    parts.append("</svg>")
    return "\n".join(parts)


def _board(mode, colors, data, rows, width, columns):
    """Five languages on each row. Wide is the same board with longer bars."""
    rows = (rows or [["No languages", 0]])[:10]
    margin = 20
    gap = 18 if width > 600 else 12
    track = (width - margin * 2 - gap * (columns - 1)) / columns
    per = (len(rows) + columns - 1) // columns
    pitch = 78 if width > 600 else 64
    top = 72
    height = top + per * pitch + 4
    name, _ = dots("LANGUAGES", margin + 16, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, width, height, f"{data['login']} languages"), name]
    pct_size = 22 if width > 600 else 16
    for index, (lang, share) in enumerate(rows):
        column = index % columns
        row = index // columns
        x = margin + column * (track + gap)
        y = top + row * pitch
        parts.append(label(x, y, lang, colors["fg"], 13 if width > 600 else 12, 0.05))
        parts.append(label(x, y + (28 if width > 600 else 22), _pct(share), colors["figure"], pct_size, -0.4))
        parts.append(_share_bar(x, y + (40 if width > 600 else 32), track, share, colors))
    parts.append("</svg>")
    return "\n".join(parts)


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/{card}?username={login}&theme={mode}&size={size}"
    return [
        f"**{card}** · {mode} · {size}",
        "",
        f"`{url}`",
        "",
        f"![{card} {mode} {size}](dist/{login}/{filename})",
        "",
    ]


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = languages(login)
    data["login"] = login
    out = ROOT / "dist" / login
    out.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {login}",
        "",
        "Each bar is that language's own share. Mini lists five. Compact lists ten in two columns. Regular and wide put five languages on each of two rows.",
        "",
    ]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += _variant("languages", login, mode, size, filename)
            print(login, mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
