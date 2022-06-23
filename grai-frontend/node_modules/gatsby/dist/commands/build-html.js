"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.buildHTMLPagesAndDeleteStaleArtifacts = buildHTMLPagesAndDeleteStaleArtifacts;
exports.buildHTML = exports.doBuildPages = exports.deleteRenderer = exports.buildRenderer = exports.getDevSSRWebpack = void 0;

var _bluebird = _interopRequireDefault(require("bluebird"));

var _fsExtra = _interopRequireDefault(require("fs-extra"));

var _reporter = _interopRequireDefault(require("gatsby-cli/lib/reporter"));

var _errors = require("gatsby-cli/lib/reporter/errors");

var _lodash = require("lodash");

var _bundle = require("../utils/webpack/bundle");

var path = _interopRequireWildcard(require("path"));

var _redux = require("../redux");

var _webpack = _interopRequireDefault(require("webpack"));

var _webpack2 = _interopRequireDefault(require("../utils/webpack.config"));

var _webpackErrorUtils = require("../utils/webpack-error-utils");

var buildUtils = _interopRequireWildcard(require("./build-utils"));

var _getPageData = require("../utils/get-page-data");

var _types = require("./types");

var _constants = require("../constants");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

// TODO
const isPreview = process.env.GATSBY_IS_PREVIEW === `true`;
let devssrWebpackCompiler;
let needToRecompileSSRBundle = true;

const getDevSSRWebpack = () => {
  if (process.env.gatsby_executing_command !== `develop`) {
    throw new Error(`This function can only be called in development`);
  }

  return {
    devssrWebpackWatcher: devssrWebpackCompiler,
    devssrWebpackCompiler: devssrWebpackCompiler.compiler,
    needToRecompileSSRBundle
  };
};

exports.getDevSSRWebpack = getDevSSRWebpack;
let oldHash = ``;
let newHash = ``;

const runWebpack = (compilerConfig, stage, directory) => {
  const isDevSSREnabledAndViable = process.env.GATSBY_EXPERIMENTAL_DEV_SSR && stage === `develop-html`;
  return new Promise((resolve, reject) => {
    if (isDevSSREnabledAndViable) {
      const compiler = (0, _webpack.default)(compilerConfig); // because of this line we can't use our watch helper
      // These things should use emitter

      compiler.hooks.invalid.tap(`ssr file invalidation`, () => {
        needToRecompileSSRBundle = true;
      });
      const watcher = compiler.watch({
        ignored: /node_modules/
      }, (err, stats) => {
        // this runs multiple times
        needToRecompileSSRBundle = false;

        _redux.emitter.emit(`DEV_SSR_COMPILATION_DONE`);

        watcher.suspend();

        if (err) {
          return reject(err);
        } else {
          newHash = (stats === null || stats === void 0 ? void 0 : stats.hash) || ``;

          const {
            restartWorker
          } = require(`../utils/dev-ssr/render-dev-html`); // Make sure we use the latest version during development


          if (oldHash !== `` && newHash !== oldHash) {
            restartWorker(`${directory}/${_constants.ROUTES_DIRECTORY}render-page.js`);
          }

          oldHash = newHash;
          return resolve({
            stats: stats,
            close: () => new Promise((resolve, reject) => watcher.close(err => err ? reject(err) : resolve()))
          });
        }
      });
      devssrWebpackCompiler = watcher;
    } else {
      (0, _bundle.build)(compilerConfig).then(({
        stats,
        close
      }) => {
        resolve({
          stats,
          close
        });
      }, err => reject(err));
    }
  });
};

const doBuildRenderer = async (directory, webpackConfig, stage) => {
  const {
    stats,
    close
  } = await runWebpack(webpackConfig, stage, directory);

  if (stats !== null && stats !== void 0 && stats.hasErrors()) {
    _reporter.default.panicOnBuild((0, _webpackErrorUtils.structureWebpackErrors)(stage, stats.compilation.errors));
  } // render-page.js is hard coded in webpack.config


  return {
    rendererPath: `${directory}/${_constants.ROUTES_DIRECTORY}render-page.js`,
    stats,
    close
  };
};

const buildRenderer = async (program, stage, parentSpan) => {
  const config = await (0, _webpack2.default)(program, program.directory, stage, null, {
    parentSpan
  });
  return doBuildRenderer(program.directory, config, stage);
}; // TODO remove after v4 release and update cloud internals


exports.buildRenderer = buildRenderer;

const deleteRenderer = async rendererPath => {
  try {
    await _fsExtra.default.remove(rendererPath);
    await _fsExtra.default.remove(`${rendererPath}.map`);
  } catch (e) {// This function will fail on Windows with no further consequences.
  }
};

exports.deleteRenderer = deleteRenderer;

const renderHTMLQueue = async (workerPool, activity, htmlComponentRendererPath, pages, stage = _types.Stage.BuildHTML) => {
  // We need to only pass env vars that are set programmatically in gatsby-cli
  // to child process. Other vars will be picked up from environment.
  const envVars = [[`NODE_ENV`, process.env.NODE_ENV], [`gatsby_executing_command`, process.env.gatsby_executing_command], [`gatsby_log_level`, process.env.gatsby_log_level]];
  const segments = (0, _lodash.chunk)(pages, 50);
  const sessionId = Date.now();

  const {
    webpackCompilationHash
  } = _redux.store.getState();

  const renderHTML = stage === `build-html` ? workerPool.single.renderHTMLProd : workerPool.single.renderHTMLDev;
  const uniqueUnsafeBuiltinUsedStacks = new Set();

  try {
    await _bluebird.default.map(segments, async pageSegment => {
      const renderHTMLResult = await renderHTML({
        envVars,
        htmlComponentRendererPath,
        paths: pageSegment,
        sessionId,
        webpackCompilationHash
      });

      if (isPreview) {
        const htmlRenderMeta = renderHTMLResult;
        const seenErrors = new Set();
        const errorMessages = new Map();
        await Promise.all(Object.entries(htmlRenderMeta.previewErrors).map(async ([pagePath, error]) => {
          if (!seenErrors.has(error.stack)) {
            errorMessages.set(error.stack, {
              pagePaths: [pagePath]
            });
            seenErrors.add(error.stack);
            const prettyError = await (0, _errors.createErrorFromString)(error.stack, `${htmlComponentRendererPath}.map`);
            const errorMessageStr = `${prettyError.stack}${prettyError.codeFrame ? `\n\n${prettyError.codeFrame}\n` : ``}`;
            const errorMessage = errorMessages.get(error.stack);
            errorMessage.errorMessage = errorMessageStr;
            errorMessages.set(error.stack, errorMessage);
          } else {
            const errorMessage = errorMessages.get(error.stack);
            errorMessage.pagePaths.push(pagePath);
            errorMessages.set(error.stack, errorMessage);
          }
        }));

        for (const value of errorMessages.values()) {
          const errorMessage = `The following page(s) saw this error when building their HTML:\n\n${value.pagePaths.map(p => `- ${p}`).join(`\n`)}\n\n${value.errorMessage}`;

          _reporter.default.error({
            id: `95314`,
            context: {
              errorMessage
            }
          });
        }
      }

      if (stage === `build-html`) {
        const htmlRenderMeta = renderHTMLResult;

        _redux.store.dispatch({
          type: `HTML_GENERATED`,
          payload: pageSegment
        });

        for (const [_pagePath, arrayOfUsages] of Object.entries(htmlRenderMeta.unsafeBuiltinsUsageByPagePath)) {
          for (const unsafeUsageStack of arrayOfUsages) {
            uniqueUnsafeBuiltinUsedStacks.add(unsafeUsageStack);
          }
        }
      }

      if (activity && activity.tick) {
        activity.tick(pageSegment.length);
      }
    });
  } catch (e) {
    var _e$context;

    if (e !== null && e !== void 0 && (_e$context = e.context) !== null && _e$context !== void 0 && _e$context.unsafeBuiltinsUsageByPagePath) {
      for (const [_pagePath, arrayOfUsages] of Object.entries(e.context.unsafeBuiltinsUsageByPagePath)) {
        // @ts-ignore TS doesn't know arrayOfUsages is Iterable
        for (const unsafeUsageStack of arrayOfUsages) {
          uniqueUnsafeBuiltinUsedStacks.add(unsafeUsageStack);
        }
      }
    }

    throw e;
  } finally {
    if (uniqueUnsafeBuiltinUsedStacks.size > 0) {
      console.warn(`Unsafe builtin method was used, future builds will need to rebuild all pages`);

      _redux.store.dispatch({
        type: `SSR_USED_UNSAFE_BUILTIN`
      });
    }

    for (const unsafeBuiltinUsedStack of uniqueUnsafeBuiltinUsedStacks) {
      const prettyError = await (0, _errors.createErrorFromString)(unsafeBuiltinUsedStack, `${htmlComponentRendererPath}.map`);
      const warningMessage = `${prettyError.stack}${prettyError.codeFrame ? `\n\n${prettyError.codeFrame}\n` : ``}`;

      _reporter.default.warn(warningMessage);
    }
  }
};

class BuildHTMLError extends Error {
  codeFrame = ``;

  constructor(error) {
    super(error.message); // We must use getOwnProperty because keys like `stack` are not enumerable,
    // but we want to copy over the entire error

    Object.getOwnPropertyNames(error).forEach(key => {
      this[key] = error[key];
    });
  }

}

const truncateObjStrings = obj => {
  // Recursively truncate strings nested in object
  // These objs can be quite large, but we want to preserve each field
  for (const key in obj) {
    if (typeof obj[key] === `object`) {
      truncateObjStrings(obj[key]);
    } else if (typeof obj[key] === `string`) {
      obj[key] = (0, _lodash.truncate)(obj[key], {
        length: 250
      });
    }
  }

  return obj;
};

const doBuildPages = async (rendererPath, pagePaths, activity, workerPool, stage) => {
  try {
    await renderHTMLQueue(workerPool, activity, rendererPath, pagePaths, stage);
  } catch (error) {
    var _error$context;

    const prettyError = await (0, _errors.createErrorFromString)(error.stack, `${rendererPath}.map`);
    const buildError = new BuildHTMLError(prettyError);
    buildError.context = error.context;

    if (error !== null && error !== void 0 && (_error$context = error.context) !== null && _error$context !== void 0 && _error$context.path) {
      const pageData = await (0, _getPageData.getPageData)(error.context.path);
      const truncatedPageData = truncateObjStrings(pageData);
      const pageDataMessage = `Page data from page-data.json for the failed page "${error.context.path}": ${JSON.stringify(truncatedPageData, null, 2)}`; // This is our only error during preview so customize it a bit + add the
      // pretty build error.

      if (isPreview) {
        _reporter.default.error({
          id: `95314`,
          context: {
            pageData: pageDataMessage
          },
          error: buildError
        });
      } else {
        _reporter.default.error(pageDataMessage);
      }
    } // Don't crash the builder when we're in preview-mode.


    if (!isPreview) {
      throw buildError;
    }
  }
}; // TODO remove in v4 - this could be a "public" api


exports.doBuildPages = doBuildPages;

const buildHTML = async ({
  program,
  stage,
  pagePaths,
  activity,
  workerPool
}) => {
  const {
    rendererPath
  } = await buildRenderer(program, stage, activity.span);
  await doBuildPages(rendererPath, pagePaths, activity, workerPool, stage);
};

exports.buildHTML = buildHTML;

async function buildHTMLPagesAndDeleteStaleArtifacts({
  workerPool,
  parentSpan,
  program
}) {
  const pageRenderer = `${program.directory}/${_constants.ROUTES_DIRECTORY}render-page.js`;
  buildUtils.markHtmlDirtyIfResultOfUsedStaticQueryChanged();
  const {
    toRegenerate,
    toDelete,
    toCleanupFromTrackedState
  } = buildUtils.calcDirtyHtmlFiles(_redux.store.getState());

  _redux.store.dispatch({
    type: `HTML_TRACKED_PAGES_CLEANUP`,
    payload: toCleanupFromTrackedState
  });

  if (toRegenerate.length > 0) {
    const buildHTMLActivityProgress = _reporter.default.createProgress(`Building static HTML for pages`, toRegenerate.length, 0, {
      parentSpan
    });

    buildHTMLActivityProgress.start();

    try {
      await doBuildPages(pageRenderer, toRegenerate, buildHTMLActivityProgress, workerPool, _types.Stage.BuildHTML);
    } catch (err) {
      let id = `95313`; // TODO: verify error IDs exist

      const context = {
        errorPath: err.context && err.context.path,
        ref: ``
      };
      const match = err.message.match(/ReferenceError: (window|document|localStorage|navigator|alert|location) is not defined/i);

      if (match && match[1]) {
        id = `95312`;
        context.ref = match[1];
      }

      buildHTMLActivityProgress.panic({
        id,
        context,
        error: err
      });
    }

    buildHTMLActivityProgress.end();
  } else {
    _reporter.default.info(`There are no new or changed html files to build.`);
  }

  if ("4" !== `4` && !program.keepPageRenderer) {
    try {
      await deleteRenderer(pageRenderer);
    } catch (err) {// pass through
    }
  }

  if (toDelete.length > 0) {
    const publicDir = path.join(program.directory, `public`);

    const deletePageDataActivityTimer = _reporter.default.activityTimer(`Delete previous page data`);

    deletePageDataActivityTimer.start();
    await buildUtils.removePageFiles(publicDir, toDelete);
    deletePageDataActivityTimer.end();
  }

  return {
    toRegenerate,
    toDelete
  };
}
//# sourceMappingURL=build-html.js.map