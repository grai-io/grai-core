"use strict";

exports.__esModule = true;
exports.generatePageTree = generatePageTree;

function generatePageTree(collections, LIMIT = 8) {
  const SSGIterator = collections.SSG.values();
  const DSGIterator = collections.DSG.values();
  const SSRIterator = collections.SSR.values();
  const FNIterator = collections.FN.values();
  const SSGPages = generateLineUntilLimit(SSGIterator, ` `, LIMIT / 4, collections.SSG.size);
  const DSGPages = generateLineUntilLimit(DSGIterator, `D`, LIMIT / 4, collections.DSG.size);
  const SSRPages = generateLineUntilLimit(SSRIterator, `∞`, LIMIT / 4, collections.SSR.size);
  const FNPages = generateLineUntilLimit(FNIterator, `λ`, LIMIT / 4, collections.FN.size); // TODO if not all the 8 lines are taken we should fill it up with the rest of the pages (each component should have LIMIT lines)

  return SSGPages.concat(DSGPages).concat(SSRPages).concat(FNPages);
}

function generateLineUntilLimit(iterator, symbol, limit, max) {
  const pages = [];

  for (let item = iterator.next(); !item.done && pages.length < limit; item = iterator.next()) {
    pages.push({
      text: item.value,
      symbol
    });
  }

  if (pages.length < max) {
    pages[pages.length - 1].text = `...${max - pages.length + 1} more pages available`;
  }

  return pages;
}