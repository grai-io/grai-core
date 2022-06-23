"use strict";

var _core = require("@babel/core");

var nodeApis = _interopRequireWildcard(require("../../utils/api-node-docs"));

var _printPlugins = require("./print-plugins");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

const apisToKeep = new Set(_printPlugins.schemaCustomizationAPIs);
apisToKeep.add(`onPluginInit`);

module.exports = function loader(source) {
  const result = (0, _core.transformSync)(source, {
    babelrc: false,
    configFile: false,
    plugins: [[require.resolve(`../../utils/babel/babel-plugin-remove-api`), {
      apis: Object.keys(nodeApis).filter(api => !apisToKeep.has(api))
    }]]
  });
  return result === null || result === void 0 ? void 0 : result.code;
};
//# sourceMappingURL=webpack-remove-apis-loader.js.map