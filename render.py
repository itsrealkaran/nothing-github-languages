"""Language card. A bar shows each share. The lead language is the figure."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import languages
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data, border=True):
    colors = theme(mode)
    rows = data["languages"][:10] or [["No languages", 0]]
    if size == "mini":
        return _mini(mode, colors, data, rows[:5], border)
    if size == "compact":
        return _columns(mode, colors, data, rows, border)
    if size == "wide":
        return _lead(mode, colors, data, rows, 896, 240, border)
    return _lead(mode, colors, data, rows, 440, 248, border)


def _pct(share):
    if share and share < 0.1:
        return f"{share:.2f}%"
    return f"{share:.1f}%"


def _share_bar(x, y, track, share, colors):
    filled = track * (share / 100) if share else 0
    if share and filled < 3:
        filled = 3
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{track:.1f}" height="6" fill="{colors["rule"]}"/>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{filled:.1f}" height="6" fill="{colors["figure"]}"/>'
    )


def _mini(mode, colors, data, rows, border):
    lead, share = rows[0]
    rest = rows[1:]
    name, _ = dots("LANGUAGES", 28, 12, colors["fg"], scale=1.15)
    parts = [
        open_svg(mode, 220, 228, f"{data['login']} languages", mark=6, margin=14, border=border),
        name,
        label(14, 78, _pct(share).rstrip("%"), colors["figure"], 28, -0.8),
        label(14, 96, lead, colors["muted"], 11, 0.2),
        _share_bar(14, 106, 192, share, colors),
    ]
    for index, (lang, part) in enumerate(rest):
        y = 138 + index * 22
        parts.append(label(14, y, lang, colors["fg"], 11, 0.05))
        parts.append(label(206, y, _pct(part), colors["figure"], 11, 0, anchor="end"))
        parts.append(_share_bar(118, y - 9, 48, part, colors))
    parts.append("</svg>")
    return "\n".join(parts)


def _columns(mode, colors, data, rows, border):
    """Ten languages, two columns. The bar under each name is that language's share."""
    margin = 20
    gap = 28
    width = 495
    track = (width - margin * 2 - gap) / 2
    per = 5
    pitch = 46
    top = 68
    height = top + per * pitch + 6
    name, _ = dots("LANGUAGES", margin + 16, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, width, height, f"{data['login']} languages", border=border), name]
    for index, (lang, share) in enumerate(rows):
        column = index // per
        row = index % per
        x = margin + column * (track + gap)
        y = top + row * pitch
        parts.append(label(x, y, lang, colors["fg"], 13, 0.05))
        parts.append(label(x + track, y, _pct(share), colors["figure"], 13, 0, anchor="end"))
        parts.append(_share_bar(x, y + 8, track, share, colors))
    parts.append("</svg>")
    return "\n".join(parts)


def _lead(mode, colors, data, rows, width, height, border):
    """The first language is the figure. The rest sit in rows beside it."""
    lead, share = rows[0]
    rest = rows[1:]
    wide = width > 600
    name, _ = dots("LANGUAGES", 36, 16, colors["fg"], scale=1.8)
    number = 52 if wide else 40
    parts = [
        open_svg(mode, width, height, f"{data['login']} languages", border=border),
        name,
        label(20, 118 if wide else 112, _pct(share).rstrip("%"), colors["figure"], number, -1.2),
        label(20, 146 if wide else 136, lead, colors["muted"], 13, 0.2),
        _share_bar(20, 164 if wide else 152, 284 if wide else 160, share, colors),
    ]
    columns = 2 if wide else 1
    per = (len(rest) + columns - 1) // columns
    origin = 320 if wide else 196
    gutter = 48 if wide else 0
    span = (width - origin - 20 - gutter * (columns - 1)) / columns
    pitch = 32 if wide else 18
    top = 78
    for index, (lang, part) in enumerate(rest):
        column = index // per
        row = index % per
        x = origin + column * (span + gutter)
        y = top + row * pitch
        parts.append(
            f'<rect x="{x:.1f}" y="{y - 10}" width="5" height="5" fill="{colors["mark"]}"/>'
        )
        parts.append(label(x + 12, y, lang, colors["fg"], 13, 0.05))
        if wide:
            parts.append(_share_bar(x + 118, y - 11, 72, part, colors))
        parts.append(label(x + span - 8, y, _pct(part), colors["figure"], 13, 0, anchor="end"))
    parts.append("</svg>")
    return "\n".join(parts)


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/nothing-github-languages?username={login}&theme={mode}&size={size}"
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
        "The first language is the figure, and a bar shows its share. Compact lists ten languages in two columns. Mini lists five.",
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
