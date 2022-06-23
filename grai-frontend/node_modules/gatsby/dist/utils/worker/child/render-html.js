"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.renderHTMLDev = exports.renderHTMLProd = void 0;

var _fsExtra = _interopRequireDefault(require("fs-extra"));

var _bluebird = _interopRequireDefault(require("bluebird"));

var path = _interopRequireWildcard(require("path"));

var _gatsbyCoreUtils = require("gatsby-core-utils");

var _lodash = require("lodash");

var _clientAssetsForTemplate = require("../../client-assets-for-template");

var _pageData = require("../../page-data");

var _staticQueryUtils = require("../../static-query-utils");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

/* eslint-disable @typescript-eslint/no-namespace */
// we want to force posix-style joins, so Windows doesn't produce backslashes for urls
const {
  join
} = path.posix;

/**
 * Used to track if renderHTMLProd / renderHTMLDev are called within same "session" (from same renderHTMLQueue call).
 * As long as sessionId remains the same we can rely on memoized/cached resources for templates, css file content for inlining and static query results.
 * If session changes we invalidate our memoization caches.
 */
let lastSessionId = 0;
let htmlComponentRenderer;
let webpackStats;
const resourcesForTemplateCache = new Map();
const inFlightResourcesForTemplate = new Map();

function clearCaches() {
  (0, _staticQueryUtils.clearStaticQueryCaches)();
  resourcesForTemplateCache.clear();
  inFlightResourcesForTemplate.clear();
  (0, _clientAssetsForTemplate.clearCache)();
}

async function doGetResourcesForTemplate(pageData) {
  const scriptsAndStyles = await (0, _clientAssetsForTemplate.getScriptsAndStylesForTemplate)(pageData.componentChunkName, webpackStats);
  const {
    staticQueryContext
  } = await (0, _staticQueryUtils.getStaticQueryContext)(pageData.staticQueryHashes);
  return {
    staticQueryContext,
    ...scriptsAndStyles
  };
}

async function getResourcesForTemplate(pageData) {
  const memoizedResourcesForTemplate = resourcesForTemplateCache.get(pageData.componentChunkName);

  if (memoizedResourcesForTemplate) {
    return memoizedResourcesForTemplate;
  }

  const inFlight = inFlightResourcesForTemplate.get(pageData.componentChunkName);

  if (inFlight) {
    return inFlight;
  }

  const doWorkPromise = doGetResourcesForTemplate(pageData);
  inFlightResourcesForTemplate.set(pageData.componentChunkName, doWorkPromise);
  const resources = await doWorkPromise;
  resourcesForTemplateCache.set(pageData.componentChunkName, resources);
  inFlightResourcesForTemplate.delete(pageData.componentChunkName);
  return resources;
}

const truncateObjStrings = obj => {
  // Recursively truncate strings nested in object
  // These objs can be quite large, but we want to preserve each field
  for (const key in obj) {
    if (typeof obj[key] === `object` && obj[key] !== null) {
      truncateObjStrings(obj[key]);
    } else if (typeof obj[key] === `string`) {
      obj[key] = (0, _lodash.truncate)(obj[key], {
        length: 250
      });
    }
  }

  return obj;
};

const renderHTMLProd = async ({
  htmlComponentRendererPath,
  paths,
  envVars,
  sessionId,
  webpackCompilationHash
}) => {
  const publicDir = join(process.cwd(), `public`);
  const isPreview = process.env.GATSBY_IS_PREVIEW === `true`;
  const unsafeBuiltinsUsageByPagePath = {};
  const previewErrors = {}; // Check if we need to do setup and cache clearing. Within same session we can reuse memoized data,
  // but it's not safe to reuse them in different sessions. Check description of `lastSessionId` for more details

  if (sessionId !== lastSessionId) {
    clearCaches(); // This is being executed in child process, so we need to set some vars
    // for modules that aren't bundled by webpack.

    envVars.forEach(([key, value]) => process.env[key] = value);
    htmlComponentRenderer = require(htmlComponentRendererPath);
    webpackStats = await (0, _clientAssetsForTemplate.readWebpackStats)(publicDir);
    lastSessionId = sessionId;

    if (global.unsafeBuiltinUsage && global.unsafeBuiltinUsage.length > 0) {
      unsafeBuiltinsUsageByPagePath[`__import_time__`] = global.unsafeBuiltinUsage;
    }
  }

  await _bluebird.default.map(paths, async pagePath => {
    try {
      const pageData = await (0, _pageData.readPageData)(publicDir, pagePath);
      const resourcesForTemplate = await getResourcesForTemplate(pageData);
      const {
        html,
        unsafeBuiltinsUsage
      } = await htmlComponentRenderer.default({
        pagePath,
        pageData,
        webpackCompilationHash,
        ...resourcesForTemplate
      });

      if (unsafeBuiltinsUsage.length > 0) {
        unsafeBuiltinsUsageByPagePath[pagePath] = unsafeBuiltinsUsage;
      }

      await _fsExtra.default.outputFile((0, _gatsbyCoreUtils.generateHtmlPath)(publicDir, pagePath), html);
    } catch (e) {
      if (e.unsafeBuiltinsUsage && e.unsafeBuiltinsUsage.length > 0) {
        unsafeBuiltinsUsageByPagePath[pagePath] = e.unsafeBuiltinsUsage;
      } // add some context to error so we can display more helpful message


      e.context = {
        path: pagePath,
        unsafeBuiltinsUsageByPagePath
      }; // If we're in Preview-mode, write out a simple error html file.

      if (isPreview) {
        const pageData = await (0, _pageData.readPageData)(publicDir, pagePath);
        const truncatedPageData = truncateObjStrings(pageData);
        const html = `<h1>Preview build error</h1>
        <p>There was an error when building the preview page for this page ("${pagePath}").</p>
        <h3>Error</h3>
        <pre><code>${e.stack}</code></pre>
        <h3>Page component id</h3>
        <p><code>${pageData.componentChunkName}</code></p>
        <h3>Page data</h3>
        <pre><code>${JSON.stringify(truncatedPageData, null, 4)}</code></pre>`;
        await _fsExtra.default.outputFile((0, _gatsbyCoreUtils.generateHtmlPath)(publicDir, pagePath), html);
        previewErrors[pagePath] = {
          e,
          message: e.message,
          code: e.code,
          stack: e.stack,
          name: e.name
        };
      } else {
        throw e;
      }
    }
  }, {
    concurrency: 2
  });
  return {
    unsafeBuiltinsUsageByPagePath,
    previewErrors
  };
}; // TODO: remove when DEV_SSR is done


exports.renderHTMLProd = renderHTMLProd;

const renderHTMLDev = async ({
  htmlComponentRendererPath,
  paths,
  envVars,
  sessionId
}) => {
  const outputDir = join(process.cwd(), `.cache`, `develop-html`); // Check if we need to do setup and cache clearing. Within same session we can reuse memoized data,
  // but it's not safe to reuse them in different sessions. Check description of `lastSessionId` for more details

  if (sessionId !== lastSessionId) {
    clearCaches(); // This is being executed in child process, so we need to set some vars
    // for modules that aren't bundled by webpack.

    envVars.forEach(([key, value]) => process.env[key] = value);
    htmlComponentRenderer = require(htmlComponentRendererPath);
    lastSessionId = sessionId;
  }

  return _bluebird.default.map(paths, async pagePath => {
    try {
      const htmlString = await htmlComponentRenderer.default({
        pagePath
      });
      return _fsExtra.default.outputFile((0, _gatsbyCoreUtils.generateHtmlPath)(outputDir, pagePath), htmlString);
    } catch (e) {
      // add some context to error so we can display more helpful message
      e.context = {
        path: pagePath
      };
      throw e;
    }
  }, {
    concurrency: 2
  });
};

exports.renderHTMLDev = renderHTMLDev;
//# sourceMappingURL=render-html.js.map