"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.writeQueryContext = writeQueryContext;
exports.createPageSSRBundle = createPageSSRBundle;

var path = _interopRequireWildcard(require("path"));

var _webpack = _interopRequireDefault(require("webpack"));

var _module = _interopRequireDefault(require("module"));

var _webpackLogging = require("../../utils/webpack/plugins/webpack-logging");

var _clientAssetsForTemplate = require("../client-assets-for-template");

var _staticQueryUtils = require("../static-query-utils");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

const extensions = [`.mjs`, `.js`, `.json`, `.node`, `.ts`, `.tsx`];
const outputDir = path.join(process.cwd(), `.cache`, `page-ssr`);
const cacheLocation = path.join(process.cwd(), `.cache`, `webpack`, `page-ssr`);

async function writeQueryContext({
  staticQueriesByTemplate,
  components
}) {
  const waitingForWrites = [];

  for (const pageTemplate of components.values()) {
    const staticQueryHashes = staticQueriesByTemplate.get(pageTemplate.componentPath) || [];
    waitingForWrites.push((0, _staticQueryUtils.writeStaticQueryContext)(staticQueryHashes, pageTemplate.componentChunkName));
  }

  return Promise.all(waitingForWrites).then(() => {});
}

async function createPageSSRBundle({
  rootDir,
  components,
  staticQueriesByTemplate,
  webpackCompilationHash,
  reporter,
  isVerbose = false
}) {
  var _process$env$GATSBY_W;

  const webpackStats = await (0, _clientAssetsForTemplate.readWebpackStats)(path.join(rootDir, `public`));
  const toInline = {};

  for (const pageTemplate of components.values()) {
    const staticQueryHashes = staticQueriesByTemplate.get(pageTemplate.componentPath) || [];
    toInline[pageTemplate.componentChunkName] = {
      query: pageTemplate.query,
      staticQueryHashes,
      assets: await (0, _clientAssetsForTemplate.getScriptsAndStylesForTemplate)(pageTemplate.componentChunkName, webpackStats)
    };
  }

  const compiler = (0, _webpack.default)({
    name: `Page Engine`,
    mode: `none`,
    entry: path.join(__dirname, `entry.js`),
    output: {
      path: outputDir,
      filename: `index.js`,
      libraryTarget: `commonjs`
    },
    target: `node`,
    externalsPresets: {
      node: false
    },
    cache: {
      type: `filesystem`,
      name: `page-ssr`,
      cacheLocation,
      buildDependencies: {
        config: [__filename]
      }
    },
    // those are required in some runtime paths, but we don't need them
    externals: [/^\.\/routes/, `electron`, // :shrug: `got` seems to have electron specific code path
    _module.default.builtinModules.reduce((acc, builtinModule) => {
      if (builtinModule === `fs`) {
        acc[builtinModule] = `global _actualFsWrapper`;
      } else {
        acc[builtinModule] = `commonjs ${builtinModule}`;
      }

      return acc;
    }, {})],
    devtool: false,
    module: {
      rules: [{
        test: /\.m?js$/,
        type: `javascript/auto`,
        resolve: {
          byDependency: {
            esm: {
              fullySpecified: false
            }
          }
        }
      }, {
        // For node binary relocations, include ".node" files as well here
        test: /\.(m?js|node)$/,
        // it is recommended for Node builds to turn off AMD support
        parser: {
          amd: false
        },
        use: {
          loader: require.resolve(`@vercel/webpack-asset-relocator-loader`),
          options: {
            outputAssetBase: `assets`
          }
        }
      }, {
        test: /\.txt/,
        type: `asset/resource`
      }]
    },
    resolve: {
      extensions,
      alias: {
        ".cache": `${rootDir}/.cache/`,
        [require.resolve(`gatsby-cli/lib/reporter/loggers/ink/index.js`)]: false,
        inquirer: false
      }
    },
    plugins: [new _webpack.default.DefinePlugin({
      INLINED_TEMPLATE_TO_DETAILS: JSON.stringify(toInline),
      WEBPACK_COMPILATION_HASH: JSON.stringify(webpackCompilationHash),
      // eslint-disable-next-line @typescript-eslint/naming-convention
      "process.env.GATSBY_LOGGER": JSON.stringify(`yurnalist`)
    }), (_process$env$GATSBY_W = process.env.GATSBY_WEBPACK_LOGGING) !== null && _process$env$GATSBY_W !== void 0 && _process$env$GATSBY_W.includes(`page-engine`) ? new _webpackLogging.WebpackLoggingPlugin(rootDir, reporter, isVerbose) : false].filter(Boolean)
  });
  return new Promise((resolve, reject) => {
    compiler.run((err, stats) => {
      compiler.close(closeErr => {
        if (err) {
          return reject(err);
        }

        if (closeErr) {
          return reject(closeErr);
        }

        return resolve(stats === null || stats === void 0 ? void 0 : stats.compilation);
      });
    });
  });
}
//# sourceMappingURL=bundle-webpack.js.map