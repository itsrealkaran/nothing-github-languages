"""Language card. Every size lists languages. Each bar is that language's share of the code."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import languages
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    colors = theme(mode)
    if size == "mini":
        return _legend(mode, colors, data, data["languages"][:5], 220, 1, mark=6, margin=14)
    if size == "compact":
        return _legend(mode, colors, data, data["languages"][:10], 495, 2)
    if size == "wide":
        return _wide(mode, colors, data)
    return _rows(mode, colors, data, data["languages"], 495, 20, 250)


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


def _stack(x, y, track, rows, colors):
    widths = []
    for _, share in rows:
        width = track * (share / 100) if share else 0
        if share and width < 2:
            width = 2
        widths.append(width)
    total = sum(widths)
    if total > track and total:
        widths = [width * track / total for width in widths]
    parts = [f'<rect x="{x}" y="{y}" width="{track}" height="8" fill="{colors["rule"]}"/>']
    cursor = x
    for width in widths:
        if width <= 0:
            continue
        draw = width - 1.5 if width > 3 else width
        parts.append(
            f'<rect x="{cursor:.1f}" y="{y}" width="{draw:.1f}" height="8" fill="{colors["figure"]}"/>'
        )
        cursor += width
    return "".join(parts)


def _item(x, y, lang, share, colors, size):
    return "\n".join([
        f'<rect x="{x}" y="{y - 9}" width="6" height="6" fill="{colors["mark"]}"/>',
        label(x + 12, y, f"{lang} {_pct(share)}", colors["fg"], size, 0.05),
    ])


def _legend(mode, colors, data, rows, width, columns, mark=8, margin=20):
    rows = rows or [["No languages", 0]]
    per = (len(rows) + columns - 1) // columns
    narrow = width < 300
    bar_y = 46 if narrow else 54
    pitch = 20 if narrow else 22
    height = bar_y + 28 + per * pitch + 8
    name, _ = dots(
        "LANGUAGES",
        margin + 16,
        12 if narrow else 16,
        colors["fg"],
        scale=1.15 if narrow else 1.8,
    )
    parts = [
        open_svg(mode, width, height, f"{data['login']} languages", mark=mark, margin=margin),
        name,
        _stack(margin, bar_y, width - margin * 2, rows, colors),
    ]
    span = (width - margin * 2) / columns
    for index, (lang, share) in enumerate(rows):
        column = index // per
        row = index % per
        x = margin + column * span
        y = bar_y + 28 + row * pitch
        parts.append(_item(x, y, lang, share, colors, 11 if narrow else 13))
    parts.append("</svg>")
    return "\n".join(parts)


def _rows(mode, colors, data, rows, width, pad, track, mark=8, margin=20):
    rows = rows or [["No languages", 0]]
    pitch = 28
    height = 64 + len(rows) * pitch + 8
    name, _ = dots("LANGUAGES", margin + 16, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, width, height, f"{data['login']} languages", mark=mark, margin=margin), name]
    for index, (lang, share) in enumerate(rows):
        y = 72 + index * pitch
        bar_x = width - pad - track
        parts.append(label(pad, y, lang, colors["fg"], 13, 0.1))
        parts.append(label(bar_x - 12, y, _pct(share), colors["muted"], 12, 0.2, anchor="end"))
        parts.append(_share_bar(bar_x, y - 10, track, share, colors))
    parts.append("</svg>")
    return "\n".join(parts)


def _wide(mode, colors, data):
    rows = (data["languages"] or [["No languages", 0]])[:8]
    lead, share = rows[0]
    name, _ = dots("LANGUAGES", 40, 16, colors["fg"], scale=1.8)
    parts = [
        open_svg(mode, 896, 268, f"{data['login']} languages"),
        name,
        label(20, 118, f"{share:.0f}%", colors["figure"], 48, -1),
        label(20, 146, lead, colors["fg"], 16, 0.2),
        _share_bar(20, 164, 250, share, colors),
        label(20, 188, "of the code", colors["muted"], 12, 0.3),
    ]
    rest = rows[1:]
    for index, (lang, part) in enumerate(rest):
        column = index // 4
        row = index % 4
        x = 310 + column * 290
        y = 92 + row * 36
        parts.append(label(x, y, lang, colors["fg"], 13, 0.1))
        parts.append(label(x + 180, y, _pct(part), colors["muted"], 12, 0.2, anchor="end"))
        parts.append(_share_bar(x, y + 8, 180, part, colors))
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
        "Mini and compact are one share bar and a language list, with no footer. Regular lists each language on its own bar. Wide leads with the largest share.",
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
