"use strict";

const { dots, label, openSvg } = require("./frame");
const { theme } = require("./nothing");
const { add, div, f, fixed, mul, pyRound } = require("./format");

function render(mode, size, data, border = true) {
  const colors = theme(mode);
  const rows = (data.languages || []).slice(0, 10);
  const list = rows.length ? rows : [["No languages", 0]];
  if (size === "mini") return mini(mode, colors, data, list.slice(0, 5), border);
  if (size === "compact") return columns(mode, colors, data, list, border);
  if (size === "wide") return lead(mode, colors, data, list, 896, 240, border);
  return lead(mode, colors, data, list, 440, 248, border);
}

function pct(share) {
  if (share && share < 0.1) return fixed(share, 2) + "%";
  return fixed(share, 1) + "%";
}

function shareBar(x, y, track, share, colors) {
  let filled = share ? mul(track, div(share, 100)) : 0;
  if (share && filled.n < 3) filled = f(3);
  return (
    `<rect x="${fixed(x, 1)}" y="${fixed(y, 1)}" width="${fixed(track, 1)}" height="6" fill="${colors.rule}"/>` +
    `<rect x="${fixed(x, 1)}" y="${fixed(y, 1)}" width="${fixed(filled, 1)}" height="6" fill="${colors.figure}"/>`
  );
}

function mini(mode, colors, data, rows, border) {
  const [leadName, share] = rows[0];
  const rest = rows.slice(1);
  const [name] = dots("LANGUAGES", 28, 12, colors.fg, 1.15);
  const parts = [
    openSvg(mode, 220, 228, data.login + " languages", 6, 14, border),
    name,
    label(14, 78, pct(share).replace(/%$/, ""), colors.figure, 28, -0.8),
    label(14, 96, leadName, colors.muted, 11, 0.2),
    shareBar(14, 106, 192, share, colors),
  ];
  rest.forEach(([lang, part], index) => {
    const y = 138 + index * 22;
    parts.push(label(14, y, lang, colors.fg, 11, 0.05));
    parts.push(label(206, y, pct(part), colors.figure, 11, 0, "end"));
    parts.push(shareBar(118, y - 9, 48, part, colors));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

function columns(mode, colors, data, rows, border) {
  const margin = 20;
  const gap = 28;
  const width = 495;
  const track = div(width - margin * 2 - gap, 2);
  const per = 5;
  const pitch = 46;
  const top = 68;
  const height = top + per * pitch + 6;
  const [name] = dots("LANGUAGES", margin + 16, 16, colors.fg, 1.8);
  const parts = [openSvg(mode, width, height, data.login + " languages", 8, 20, border), name];
  rows.forEach(([lang, share], index) => {
    const column = Math.floor(index / per);
    const row = index % per;
    const x = add(margin, mul(column, add(track, gap)));
    const y = top + row * pitch;
    parts.push(label(x, y, lang, colors.fg, 13, 0.05));
    parts.push(label(add(x, track), y, pct(share), colors.figure, 13, 0, "end"));
    parts.push(shareBar(x, y + 8, track, share, colors));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

function lead(mode, colors, data, rows, width, height, border) {
  const [leadName, share] = rows[0];
  const rest = rows.slice(1);
  const wide = width > 600;
  const [name] = dots("LANGUAGES", 36, 16, colors.fg, 1.8);
  const number = wide ? 52 : 40;
  const parts = [
    openSvg(mode, width, height, data.login + " languages", 8, 20, border),
    name,
    label(20, wide ? 118 : 112, pct(share).replace(/%$/, ""), colors.figure, number, -1.2),
    label(20, wide ? 146 : 136, leadName, colors.muted, 13, 0.2),
    shareBar(20, wide ? 164 : 152, wide ? 284 : 160, share, colors),
  ];
  const columns = wide ? 2 : 1;
  const per = Math.floor((rest.length + columns - 1) / columns);
  const origin = wide ? 320 : 196;
  const gutter = wide ? 48 : 0;
  const span = div(width - origin - 20 - gutter * (columns - 1), columns);
  const pitch = wide ? 32 : 18;
  const top = 78;
  rest.forEach(([lang, part], index) => {
    const column = per ? Math.floor(index / per) : 0;
    const row = per ? index % per : 0;
    const x = add(origin, mul(column, add(span, gutter)));
    const y = top + row * pitch;
    parts.push(`<rect x="${fixed(x, 1)}" y="${pyInt(y - 10)}" width="5" height="5" fill="${colors.mark}"/>`);
    parts.push(label(add(x, 12), y, lang, colors.fg, 13, 0.05));
    if (wide) parts.push(shareBar(add(x, 118), y - 11, 72, part, colors));
    parts.push(label(add(add(x, span), -8), y, pct(part), colors.figure, 13, 0, "end"));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

function pyInt(value) {
  return String(value);
}

module.exports = { render, pyRound };
