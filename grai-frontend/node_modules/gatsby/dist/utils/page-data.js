"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.readPageData = readPageData;
exports.removePageData = removePageData;
exports.pageDataExists = pageDataExists;
exports.waitUntilPageQueryResultsAreStored = waitUntilPageQueryResultsAreStored;
exports.savePageQueryResult = savePageQueryResult;
exports.readPageQueryResult = readPageQueryResult;
exports.writePageData = writePageData;
exports.isFlushEnqueued = isFlushEnqueued;
exports.flush = flush;
exports.enqueueFlush = enqueueFlush;
exports.handleStalePageData = handleStalePageData;

var _fs = require("@nodelib/fs.walk");

var _fsExtra = _interopRequireDefault(require("fs-extra"));

var _reporter = _interopRequireDefault(require("gatsby-cli/lib/reporter"));

var _fastq = _interopRequireDefault(require("fastq"));

var _path = _interopRequireDefault(require("path"));

var _gatsbyCoreUtils = require("gatsby-core-utils");

var _websocketManager = require("./websocket-manager");

var _webpackStatus = require("./webpack-status");

var _redux = require("../redux");

var _queries = require("../redux/reducers/queries");

var _datastore = require("../datastore");

var _pageDataHelpers = require("./page-data-helpers");

exports.reverseFixedPagePath = _pageDataHelpers.reverseFixedPagePath;

var _nodeManifest = require("../utils/node-manifest");

var _pageMode = require("./page-mode");

async function readPageData(publicDir, pagePath) {
  const filePath = (0, _gatsbyCoreUtils.generatePageDataPath)(publicDir, pagePath);
  const rawPageData = await _fsExtra.default.readFile(filePath, `utf-8`);
  return JSON.parse(rawPageData);
}

async function removePageData(publicDir, pagePath) {
  const filePath = (0, _gatsbyCoreUtils.generatePageDataPath)(publicDir, pagePath);

  if (_fsExtra.default.existsSync(filePath)) {
    return await _fsExtra.default.remove(filePath);
  }

  return Promise.resolve();
}

function pageDataExists(publicDir, pagePath) {
  return _fsExtra.default.existsSync((0, _gatsbyCoreUtils.generatePageDataPath)(publicDir, pagePath));
}

let lmdbPageQueryResultsCache;

function getLMDBPageQueryResultsCache() {
  if (!lmdbPageQueryResultsCache) {
    const GatsbyCacheLmdbImpl = require(`./cache-lmdb`).default;

    lmdbPageQueryResultsCache = new GatsbyCacheLmdbImpl({
      name: `internal-tmp-query-results`,
      encoding: `string`
    }).init();
  }

  return lmdbPageQueryResultsCache;
}

let savePageQueryResultsPromise = Promise.resolve();

function waitUntilPageQueryResultsAreStored() {
  return savePageQueryResultsPromise;
}

async function savePageQueryResult(programDir, pagePath, stringifiedResult) {
  if ((0, _datastore.isLmdbStore)()) {
    savePageQueryResultsPromise = getLMDBPageQueryResultsCache().set(pagePath, stringifiedResult);
  } else {
    const pageQueryResultsPath = _path.default.join(programDir, `.cache`, `json`, `${pagePath.replace(/\//g, `_`)}.json`);

    await _fsExtra.default.outputFile(pageQueryResultsPath, stringifiedResult);
  }
}

async function readPageQueryResult(publicDir, pagePath) {
  if ((0, _datastore.isLmdbStore)()) {
    const stringifiedResult = await getLMDBPageQueryResultsCache().get(pagePath);

    if (typeof stringifiedResult === `string`) {
      return stringifiedResult;
    }

    throw new Error(`Couldn't find temp query result for "${pagePath}".`);
  } else {
    const pageQueryResultsPath = _path.default.join(publicDir, `..`, `.cache`, `json`, `${pagePath.replace(/\//g, `_`)}.json`);

    return _fsExtra.default.readFile(pageQueryResultsPath);
  }
}

async function writePageData(publicDir, pageData) {
  const result = await readPageQueryResult(publicDir, pageData.path);
  const outputFilePath = (0, _gatsbyCoreUtils.generatePageDataPath)(publicDir, pageData.path);
  const body = (0, _pageDataHelpers.constructPageDataString)(pageData, result); // transform asset size to kB (from bytes) to fit 64 bit to numbers

  const pageDataSize = Buffer.byteLength(body) / 1000;

  _redux.store.dispatch({
    type: `ADD_PAGE_DATA_STATS`,
    payload: {
      pagePath: pageData.path,
      filePath: outputFilePath,
      size: pageDataSize,
      pageDataHash: (0, _gatsbyCoreUtils.createContentDigest)(body)
    }
  });

  await _fsExtra.default.outputFile(outputFilePath, body);
  return body;
}

let isFlushPending = false;
let isFlushing = false;

function isFlushEnqueued() {
  return isFlushPending;
}

async function flush(parentSpan) {
  var _program$_;

  if (isFlushing) {
    // We're already in the middle of a flush
    return;
  }

  await waitUntilPageQueryResultsAreStored();
  isFlushPending = false;
  isFlushing = true;

  const {
    pendingPageDataWrites,
    pages,
    program,
    staticQueriesByTemplate,
    queries
  } = _redux.store.getState();

  const isBuild = (program === null || program === void 0 ? void 0 : (_program$_ = program._) === null || _program$_ === void 0 ? void 0 : _program$_[0]) !== `develop`;
  const {
    pagePaths
  } = pendingPageDataWrites;
  let writePageDataActivity;
  let nodeManifestPagePathMap;

  if (pagePaths.size > 0) {
    // we process node manifests in this location because we need to add the manifestId to the page data.
    // We use this manifestId to determine if the page data is up to date when routing. Here we create a map of "pagePath": "manifestId" while processing and writing node manifest files.
    // We only do this when there are pending page-data writes because otherwise we could flush pending createNodeManifest calls before page-data.json files are written. Which means those page-data files wouldn't have the corresponding manifest id's written to them.
    nodeManifestPagePathMap = await (0, _nodeManifest.processNodeManifests)();
    writePageDataActivity = _reporter.default.createProgress(`Writing page-data.json files to public directory`, pagePaths.size, 0, {
      id: `write-page-data-public-directory`,
      parentSpan
    });
    writePageDataActivity.start();
  }

  const flushQueue = (0, _fastq.default)(async (pagePath, cb) => {
    const page = pages.get(pagePath); // It's a gloomy day in Bombay, let me tell you a short story...
    // Once upon a time, writing page-data.json files were atomic
    // After this change (#24808), they are not and this means that
    // between adding a pending write for a page and actually flushing
    // them, a page might not exist anymore щ（ﾟДﾟщ）
    // This is why we need this check

    if (page) {
      if (page.path && nodeManifestPagePathMap) {
        page.manifestId = nodeManifestPagePathMap.get(page.path);
      }

      if (!isBuild && process.env.GATSBY_EXPERIMENTAL_QUERY_ON_DEMAND) {
        // check if already did run query for this page
        // with query-on-demand we might have pending page-data write due to
        // changes in static queries assigned to page template, but we might not
        // have query result for it
        const query = queries.trackedQueries.get(page.path);

        if (!query) {
          // this should not happen ever
          throw new Error(`We have a page, but we don't have registered query for it (???)`);
        }

        if ((0, _queries.hasFlag)(query.dirty, _queries.FLAG_DIRTY_NEW_PAGE)) {
          // query results are not written yet
          setImmediate(() => cb(null, true));
          return;
        }
      } // In develop we rely on QUERY_ON_DEMAND so we just go through
      // In build we only build these page-json for SSG pages


      if ("4" !== `4` || !isBuild || isBuild && (0, _pageMode.getPageMode)(page) === `SSG`) {
        const staticQueryHashes = staticQueriesByTemplate.get(page.componentPath) || [];
        const result = await writePageData(_path.default.join(program.directory, `public`), { ...page,
          staticQueryHashes
        });
        writePageDataActivity.tick();

        if (!isBuild) {
          _websocketManager.websocketManager.emitPageData({
            id: pagePath,
            result: JSON.parse(result)
          });
        }
      }
    }

    _redux.store.dispatch({
      type: `CLEAR_PENDING_PAGE_DATA_WRITE`,
      payload: {
        page: pagePath
      }
    }); // `setImmediate` below is a workaround against stack overflow
    // occurring when there are many non-SSG pages


    setImmediate(() => cb(null, true));
    return;
  }, 25);

  for (const pagePath of pagePaths) {
    flushQueue.push(pagePath, () => {});
  }

  if (!flushQueue.idle()) {
    await new Promise(resolve => {
      flushQueue.drain = resolve;
    });
  }

  if (writePageDataActivity) {
    writePageDataActivity.end();
  }

  isFlushing = false;
  return;
}

function enqueueFlush(parentSpan) {
  if ((0, _webpackStatus.isWebpackStatusPending)()) {
    isFlushPending = true;
  } else {
    flush(parentSpan);
  }
}

async function handleStalePageData(parentSpan) {
  if (!(await _fsExtra.default.pathExists(`public/page-data`))) {
    return;
  } // public directory might have stale page-data files from previous builds
  // we get the list of those and compare against expected page-data files
  // and remove ones that shouldn't be there anymore


  const activity = _reporter.default.activityTimer(`Cleaning up stale page-data`, {
    parentSpan
  });

  activity.start();
  const pageDataFilesFromPreviousBuilds = await new Promise((resolve, reject) => {
    const results = new Set();
    const stream = (0, _fs.walkStream)(`public/page-data`);
    stream.on(`data`, data => {
      if (data.name === `page-data.json`) {
        results.add(data.path);
      }
    });
    stream.on(`error`, e => {
      reject(e);
    });
    stream.on(`end`, () => resolve(results));
  });
  const expectedPageDataFiles = new Set();

  _redux.store.getState().pages.forEach(page => {
    expectedPageDataFiles.add((0, _gatsbyCoreUtils.generatePageDataPath)(`public`, page.path));
  });

  const deletionPromises = [];
  pageDataFilesFromPreviousBuilds.forEach(pageDataFilePath => {
    if (!expectedPageDataFiles.has(pageDataFilePath)) {
      deletionPromises.push(_fsExtra.default.remove(pageDataFilePath));
    }
  });
  await Promise.all(deletionPromises);
  activity.end();
}
//# sourceMappingURL=page-data.js.map