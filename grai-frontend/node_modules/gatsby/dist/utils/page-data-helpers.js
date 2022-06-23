"use strict";

exports.__esModule = true;
exports.constructPageDataString = constructPageDataString;
exports.reverseFixedPagePath = reverseFixedPagePath;
exports.getPagePathFromPageDataPath = getPagePathFromPageDataPath;

function constructPageDataString({
  componentChunkName,
  matchPath,
  path: pagePath,
  staticQueryHashes,
  manifestId
}, result) {
  let body = `{
    "componentChunkName": "${componentChunkName}",
    "path": ${JSON.stringify(pagePath)},
    "result": ${result},
    "staticQueryHashes": ${JSON.stringify(staticQueryHashes)}`;

  if (matchPath) {
    body += `,
    "matchPath": "${matchPath}"`;
  }

  if (manifestId) {
    body += `,
    "manifestId": "${manifestId}"`;
  }

  body += `}`;
  return body;
}

function reverseFixedPagePath(pageDataRequestPath) {
  return pageDataRequestPath === `index` ? `/` : pageDataRequestPath;
}

function getPagePathFromPageDataPath(pageDataPath) {
  const matches = pageDataPath.matchAll(/^\/?page-data\/(.+)\/page-data.json$/gm);

  for (const [, requestedPagePath] of matches) {
    return reverseFixedPagePath(requestedPagePath);
  }

  return null;
}
//# sourceMappingURL=page-data-helpers.js.map