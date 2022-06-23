"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.getData = getData;
exports.renderPageData = renderPageData;
exports.renderHTML = renderHTML;

require("../engines-fs-provider");

var path = _interopRequireWildcard(require("path"));

var fs = _interopRequireWildcard(require("fs-extra"));

var _pageDataHelpers = require("../page-data-helpers");

var _renderPage = _interopRequireWildcard(require("./routes/render-page"));

var _getServerData = require("../get-server-data");

var _reporter = _interopRequireDefault(require("gatsby-cli/lib/reporter"));

var _tracer = require("../tracer");

var _graphqlErrorsCodeframe = require("../../query/graphql-errors-codeframe");

var _process$env$GATSBY_O;

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

const tracerReadyPromise = (0, _tracer.initTracer)((_process$env$GATSBY_O = process.env.GATSBY_OPEN_TRACING_CONFIG_FILE) !== null && _process$env$GATSBY_O !== void 0 ? _process$env$GATSBY_O : ``);

async function getData({
  pathName,
  graphqlEngine,
  req,
  spanContext,
  telemetryResolverTimings
}) {
  await tracerReadyPromise;
  let getDataWrapperActivity;

  try {
    var _serverData, _serverData2;

    if (spanContext) {
      getDataWrapperActivity = _reporter.default.phantomActivity(`Running getData`, {
        parentSpan: spanContext
      });
      getDataWrapperActivity.start();
    }

    let page;
    let templateDetails;
    let potentialPagePath;
    let findMetaActivity;

    try {
      if (getDataWrapperActivity) {
        findMetaActivity = _reporter.default.phantomActivity(`Finding details about page and template`, {
          parentSpan: getDataWrapperActivity.span
        });
        findMetaActivity.start();
      }

      potentialPagePath = (0, _pageDataHelpers.getPagePathFromPageDataPath)(pathName) || pathName; // 1. Find a page for pathname

      const maybePage = graphqlEngine.findPageByPath(potentialPagePath);

      if (!maybePage) {
        // page not found, nothing to run query for
        throw new Error(`Page for "${pathName}" not found`);
      }

      page = maybePage; // 2. Lookup query used for a page (template)

      templateDetails = INLINED_TEMPLATE_TO_DETAILS[page.componentChunkName];

      if (!templateDetails) {
        throw new Error(`Page template details for "${page.componentChunkName}" not found`);
      }
    } finally {
      if (findMetaActivity) {
        findMetaActivity.end();
      }
    }

    const executionPromises = []; // 3. Execute query
    // query-runner handles case when query is not there - so maybe we should consider using that somehow

    let results = {};
    let serverData;

    if (templateDetails.query) {
      var _runningQueryActivity;

      let runningQueryActivity;

      if (getDataWrapperActivity) {
        runningQueryActivity = _reporter.default.phantomActivity(`Running page query`, {
          parentSpan: getDataWrapperActivity.span
        });
        runningQueryActivity.start();
      }

      executionPromises.push(graphqlEngine.runQuery(templateDetails.query, { ...page,
        ...page.context
      }, {
        queryName: page.path,
        componentPath: page.componentPath,
        parentSpan: (_runningQueryActivity = runningQueryActivity) === null || _runningQueryActivity === void 0 ? void 0 : _runningQueryActivity.span,
        forceGraphqlTracing: !!runningQueryActivity,
        telemetryResolverTimings
      }).then(queryResults => {
        if (queryResults.errors && queryResults.errors.length > 0) {
          const e = queryResults.errors[0];
          const codeFrame = (0, _graphqlErrorsCodeframe.getCodeFrame)(templateDetails.query, e.locations && e.locations[0].line, e.locations && e.locations[0].column);
          const queryRunningError = new Error(e.message + `\n\n` + codeFrame);
          queryRunningError.stack = e.stack;
          throw queryRunningError;
        } else {
          results = queryResults;
        }
      }).finally(() => {
        if (runningQueryActivity) {
          runningQueryActivity.end();
        }
      }));
    } // 4. (if SSR) run getServerData


    if (page.mode === `SSR`) {
      let runningGetServerDataActivity;

      if (getDataWrapperActivity) {
        runningGetServerDataActivity = _reporter.default.phantomActivity(`Running getServerData`, {
          parentSpan: getDataWrapperActivity.span
        });
        runningGetServerDataActivity.start();
      }

      executionPromises.push((0, _renderPage.getPageChunk)(page).then(mod => (0, _getServerData.getServerData)(req, page, potentialPagePath, mod)).then(serverDataResults => {
        serverData = serverDataResults;
      }).finally(() => {
        if (runningGetServerDataActivity) {
          runningGetServerDataActivity.end();
        }
      }));
    }

    await Promise.all(executionPromises);

    if (serverData) {
      results.serverData = serverData.props;
    }

    results.pageContext = page.context;
    let searchString = ``;

    if (req !== null && req !== void 0 && req.query) {
      const maybeQueryString = Object.entries(req.query).map(([k, v]) => `${k}=${v}`).join(`&`);

      if (maybeQueryString) {
        searchString = `?${maybeQueryString}`;
      }
    }

    return {
      results,
      page,
      templateDetails,
      potentialPagePath,
      serverDataHeaders: (_serverData = serverData) === null || _serverData === void 0 ? void 0 : _serverData.headers,
      serverDataStatus: (_serverData2 = serverData) === null || _serverData2 === void 0 ? void 0 : _serverData2.status,
      searchString
    };
  } finally {
    if (getDataWrapperActivity) {
      getDataWrapperActivity.end();
    }
  }
}

function getPath(data) {
  return (data.page.mode !== `SSG` && data.page.matchPath ? data.potentialPagePath : data.page.path) + (data.page.mode === `SSR` ? data.searchString : ``);
}

async function renderPageData({
  data,
  spanContext
}) {
  await tracerReadyPromise;
  let activity;

  try {
    if (spanContext) {
      activity = _reporter.default.phantomActivity(`Rendering page-data`, {
        parentSpan: spanContext
      });
      activity.start();
    }

    const results = await (0, _pageDataHelpers.constructPageDataString)({
      componentChunkName: data.page.componentChunkName,
      path: getPath(data),
      matchPath: data.page.matchPath,
      staticQueryHashes: data.templateDetails.staticQueryHashes
    }, JSON.stringify(data.results));
    return JSON.parse(results);
  } finally {
    if (activity) {
      activity.end();
    }
  }
}

const readStaticQueryContext = async templatePath => {
  const filePath = path.join(__dirname, `sq-context`, templatePath, `sq-context.json`);
  const rawSQContext = await fs.readFile(filePath, `utf-8`);
  return JSON.parse(rawSQContext);
};

async function renderHTML({
  data,
  pageData,
  spanContext
}) {
  await tracerReadyPromise;
  let wrapperActivity;

  try {
    if (spanContext) {
      wrapperActivity = _reporter.default.phantomActivity(`Rendering HTML`, {
        parentSpan: spanContext
      });
      wrapperActivity.start();
    }

    if (!pageData) {
      var _wrapperActivity;

      pageData = await renderPageData({
        data,
        spanContext: (_wrapperActivity = wrapperActivity) === null || _wrapperActivity === void 0 ? void 0 : _wrapperActivity.span
      });
    }

    let readStaticQueryContextActivity;
    let staticQueryContext;

    try {
      if (wrapperActivity) {
        readStaticQueryContextActivity = _reporter.default.phantomActivity(`Preparing StaticQueries context`, {
          parentSpan: wrapperActivity.span
        });
        readStaticQueryContextActivity.start();
      }

      staticQueryContext = await readStaticQueryContext(data.page.componentChunkName);
    } finally {
      if (readStaticQueryContextActivity) {
        readStaticQueryContextActivity.end();
      }
    }

    let renderHTMLActivity;

    try {
      if (wrapperActivity) {
        renderHTMLActivity = _reporter.default.phantomActivity(`Actually rendering HTML`, {
          parentSpan: wrapperActivity.span
        });
        renderHTMLActivity.start();
      }

      const results = await (0, _renderPage.default)({
        pagePath: getPath(data),
        pageData,
        staticQueryContext,
        webpackCompilationHash: WEBPACK_COMPILATION_HASH,
        ...data.templateDetails.assets,
        inlinePageData: data.page.mode === `SSR` && data.results.serverData
      });
      return results.html;
    } finally {
      if (renderHTMLActivity) {
        renderHTMLActivity.end();
      }
    }
  } finally {
    if (wrapperActivity) {
      wrapperActivity.end();
    }
  }
}
//# sourceMappingURL=entry.js.map