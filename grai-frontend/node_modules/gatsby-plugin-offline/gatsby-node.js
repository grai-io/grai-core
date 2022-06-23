"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

var _extends2 = _interopRequireDefault(require("@babel/runtime/helpers/extends"));

// use `let` to workaround https://github.com/jhnns/rewire/issues/144

/* eslint-disable prefer-const */
var fs = require("fs");

var workboxBuild = require("workbox-build");

var path = require("path");

var _require = require("gatsby-core-utils"),
    slash = _require.slash;

var glob = require("glob");

var _ = require("lodash");

var getResourcesFromHTML = require("./get-resources-from-html");

exports.onPreBootstrap = function (_ref) {
  var cache = _ref.cache;
  var appShellSourcePath = path.join(__dirname, "app-shell.js");
  var appShellTargetPath = path.join(cache.directory, "app-shell.js");
  fs.copyFileSync(appShellSourcePath, appShellTargetPath);
};

exports.createPages = function (_ref2) {
  var actions = _ref2.actions,
      cache = _ref2.cache;
  var appShellPath = path.join(cache.directory, "app-shell.js");

  if (process.env.NODE_ENV === "production") {
    var createPage = actions.createPage;
    createPage({
      path: "/offline-plugin-app-shell-fallback/",
      component: slash(appShellPath)
    });
  }
};

var s;

var readStats = function readStats() {
  if (s) {
    return s;
  } else {
    s = JSON.parse(fs.readFileSync(process.cwd() + "/public/webpack.stats.json", "utf-8"));
    return s;
  }
};

function getAssetsForChunks(chunks) {
  var files = _.flatten(chunks.map(function (chunk) {
    return readStats().assetsByChunkName[chunk];
  }));

  return _.compact(files);
}

function getPrecachePages(globs, base) {
  var precachePages = [];
  globs.forEach(function (page) {
    var matches = glob.sync(base + page);
    matches.forEach(function (path) {
      var isDirectory = fs.lstatSync(path).isDirectory();
      var precachePath;

      if (isDirectory && fs.existsSync(path + "/index.html")) {
        precachePath = path + "/index.html";
      } else if (path.endsWith(".html")) {
        precachePath = path;
      } else {
        return;
      }

      if (precachePages.indexOf(precachePath) === -1) {
        precachePages.push(precachePath);
      }
    });
  });
  return precachePages;
}

exports.onPostBuild = function (args, _ref3) {
  var _ref3$precachePages = _ref3.precachePages,
      precachePagesGlobs = _ref3$precachePages === void 0 ? [] : _ref3$precachePages,
      _ref3$appendScript = _ref3.appendScript,
      appendScript = _ref3$appendScript === void 0 ? null : _ref3$appendScript,
      _ref3$debug = _ref3.debug,
      debug = _ref3$debug === void 0 ? undefined : _ref3$debug,
      _ref3$workboxConfig = _ref3.workboxConfig,
      workboxConfig = _ref3$workboxConfig === void 0 ? {} : _ref3$workboxConfig;
  var pathPrefix = args.pathPrefix,
      reporter = args.reporter;
  var rootDir = "public"; // Get exact asset filenames for app and offline app shell chunks

  var files = getAssetsForChunks(["app", "webpack-runtime", "component---node-modules-gatsby-plugin-offline-app-shell-js"]);
  var appFile = files.find(function (file) {
    return file.startsWith("app-");
  });

  function flat(arr) {
    var _ref4;

    return Array.prototype.flat ? arr.flat() : (_ref4 = []).concat.apply(_ref4, arr);
  }

  var offlineShellPath = process.cwd() + "/" + rootDir + "/offline-plugin-app-shell-fallback/index.html";
  var precachePages = [offlineShellPath].concat(getPrecachePages(precachePagesGlobs, process.cwd() + "/" + rootDir).filter(function (page) {
    return page !== offlineShellPath;
  }));

  var criticalFilePaths = _.uniq(flat(precachePages.map(function (page) {
    return getResourcesFromHTML(page, pathPrefix);
  })));

  var globPatterns = files.concat([// criticalFilePaths doesn't include HTML pages (we only need this one)
  "offline-plugin-app-shell-fallback/index.html"].concat(criticalFilePaths));
  var manifests = ["manifest.json", "manifest.webmanifest"];
  manifests.forEach(function (file) {
    if (fs.existsSync(rootDir + "/" + file)) globPatterns.push(file);
  });
  var options = {
    importWorkboxFrom: "local",
    globDirectory: rootDir,
    globPatterns: globPatterns,
    modifyURLPrefix: {
      // If `pathPrefix` is configured by user, we should replace
      // the default prefix with `pathPrefix`.
      "/": pathPrefix + "/"
    },
    cacheId: "gatsby-plugin-offline",
    // Don't cache-bust JS or CSS files, and anything in the static directory,
    // since these files have unique URLs and their contents will never change
    dontCacheBustURLsMatching: /(\.js$|\.css$|static\/)/,
    runtimeCaching: [// ignore cypress endpoints (only for testing)
    process.env.CYPRESS_SUPPORT ? {
      urlPattern: /\/__cypress\//,
      handler: "NetworkOnly"
    } : false, {
      // Use cacheFirst since these don't need to be revalidated (same RegExp
      // and same reason as above)
      urlPattern: /(\.js$|\.css$|static\/)/,
      handler: "CacheFirst"
    }, {
      // page-data.json files, static query results and app-data.json
      // are not content hashed
      urlPattern: /^https?:.*\/page-data\/.*\.json/,
      handler: "StaleWhileRevalidate"
    }, {
      // Add runtime caching of various other page resources
      urlPattern: /^https?:.*\.(png|jpg|jpeg|webp|avif|svg|gif|tiff|js|woff|woff2|json|css)$/,
      handler: "StaleWhileRevalidate"
    }, {
      // Google Fonts CSS (doesn't end in .css so we need to specify it)
      urlPattern: /^https?:\/\/fonts\.googleapis\.com\/css/,
      handler: "StaleWhileRevalidate"
    }].filter(Boolean),
    skipWaiting: true,
    clientsClaim: true
  };

  var combinedOptions = _.merge(options, workboxConfig);

  var idbKeyvalFile = "idb-keyval-iife.min.js";

  var idbKeyvalSource = require.resolve("idb-keyval/dist/" + idbKeyvalFile);

  var idbKeyvalPackageJson = require("idb-keyval/package.json");

  var idbKeyValVersioned = "idb-keyval-" + idbKeyvalPackageJson.version + "-iife.min.js";
  var idbKeyvalDest = "public/" + idbKeyValVersioned;
  fs.createReadStream(idbKeyvalSource).pipe(fs.createWriteStream(idbKeyvalDest));
  var swDest = "public/sw.js";
  return workboxBuild.generateSW((0, _extends2.default)({
    swDest: swDest
  }, combinedOptions)).then(function (_ref5) {
    var count = _ref5.count,
        size = _ref5.size,
        warnings = _ref5.warnings;
    if (warnings) warnings.forEach(function (warning) {
      return console.warn(warning);
    });

    if (debug !== undefined) {
      var swText = fs.readFileSync(swDest, "utf8").replace(/(workbox\.setConfig\({modulePathPrefix: "[^"]+")}\);/, "$1, debug: " + JSON.stringify(debug) + "});");
      fs.writeFileSync(swDest, swText);
    }

    var swAppend = fs.readFileSync(__dirname + "/sw-append.js", "utf8").replace(/%idbKeyValVersioned%/g, idbKeyValVersioned).replace(/%pathPrefix%/g, pathPrefix).replace(/%appFile%/g, appFile);
    fs.appendFileSync("public/sw.js", "\n" + swAppend);

    if (appendScript !== null) {
      var userAppend;

      try {
        userAppend = fs.readFileSync(appendScript, "utf8");
      } catch (e) {
        throw new Error("Couldn't find the specified offline inject script");
      }

      fs.appendFileSync("public/sw.js", "\n" + userAppend);
    }

    reporter.info("Generated " + swDest + ", which will precache " + count + " files, totaling " + size + " bytes.\n" + "The following pages will be precached:\n" + precachePages.map(function (path) {
      return path.replace(process.cwd() + "/public", "");
    }).join("\n"));
  });
};

var MATCH_ALL_KEYS = /^/;

exports.pluginOptionsSchema = function (_ref6) {
  var Joi = _ref6.Joi;
  // These are the options of the v3: https://www.gatsbyjs.com/plugins/gatsby-plugin-offline/#available-options
  return Joi.object({
    precachePages: Joi.array().items(Joi.string()).description("An array of pages whose resources should be precached by the service worker, using an array of globs"),
    appendScript: Joi.string().description("A file (path) to be appended at the end of the generated service worker"),
    debug: Joi.boolean().description("Specifies whether Workbox should show debugging output in the browser console at runtime. When undefined, defaults to showing debug messages on localhost only"),
    workboxConfig: Joi.object({
      importWorkboxFrom: Joi.string(),
      globDirectory: Joi.string(),
      globPatterns: Joi.array().items(Joi.string()),
      modifyURLPrefix: Joi.object().pattern(MATCH_ALL_KEYS, Joi.string()),
      cacheId: Joi.string(),
      dontCacheBustURLsMatching: Joi.object().instance(RegExp),
      maximumFileSizeToCacheInBytes: Joi.number(),
      runtimeCaching: Joi.array().items(Joi.object({
        urlPattern: Joi.object().instance(RegExp),
        handler: Joi.string().valid("StaleWhileRevalidate", "CacheFirst", "NetworkFirst", "NetworkOnly", "CacheOnly"),
        options: Joi.object({
          networkTimeoutSeconds: Joi.number()
        })
      })),
      skipWaiting: Joi.boolean(),
      clientsClaim: Joi.boolean()
    }).description("Overrides workbox configuration. Helpful documentation: https://www.gatsbyjs.com/plugins/gatsby-plugin-offline/#overriding-workbox-configuration\n      ")
  });
};