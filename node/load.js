"use strict";

const { gh, mostCommon, ownedRepos, pyRound } = require("./github");

async function load(login) {
  const owned = await ownedRepos(login);
  const totals = new Map();
  const publicTotals = new Map();
  for (const repo of owned.repos) {
    const stats = await gh("repos/" + repo.full_name + "/languages");
    add(totals, stats);
    if (!repo.private) add(publicTotals, stats);
  }
  const grand = [...totals.values()].reduce((sum, value) => sum + value, 0) || 1;
  const rows = [];
  for (const [name, amount] of mostCommon(totals)) {
    if ((publicTotals.get(name) || 0) <= 0) continue;
    rows.push([name, pyRound(100 * amount / grand, 2)]);
    if (rows.length === 10) break;
  }
  return { login, languages: rows.length ? rows : [["No languages", 0]] };
}

function add(counter, stats) {
  for (const [name, amount] of Object.entries(stats || {})) {
    counter.set(name, (counter.get(name) || 0) + amount);
  }
}

module.exports = { load };
