"use strict";

exports.__esModule = true;
exports.printQueryEnginePlugins = printQueryEnginePlugins;
exports.schemaCustomizationAPIs = void 0;

var fs = _interopRequireWildcard(require("fs-extra"));

var path = _interopRequireWildcard(require("path"));

var _ = _interopRequireWildcard(require("lodash"));

var _gatsbyCoreUtils = require("gatsby-core-utils");

var _redux = require("../../redux");

var _requireGatsbyPlugin = require("../../utils/require-gatsby-plugin");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function (nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

/* eslint @typescript-eslint/no-unused-vars: ["error", { "ignoreRestSiblings": true }] */
const schemaCustomizationAPIs = new Set([`setFieldsOnGraphQLNodeType`, `createSchemaCustomization`, `createResolvers`]);
exports.schemaCustomizationAPIs = schemaCustomizationAPIs;
const excludePlugins = new Set([`internal-data-bridge`]);
const includePlugins = new Set([`gatsby-plugin-sharp`]); // Emit file that imports required node APIs

const schemaCustomizationPluginsPath = process.cwd() + `/.cache/query-engine-plugins.js`;

async function printQueryEnginePlugins() {
  try {
    await fs.remove(schemaCustomizationPluginsPath);
  } catch (e) {// no-op
  }

  return await fs.writeFile(schemaCustomizationPluginsPath, renderQueryEnginePlugins());
}

function renderQueryEnginePlugins() {
  const {
    flattenedPlugins
  } = _redux.store.getState();

  const usedPlugins = flattenedPlugins.filter(p => includePlugins.has(p.name) || !excludePlugins.has(p.name) && p.nodeAPIs.some(api => schemaCustomizationAPIs.has(api)));
  const usedSubPlugins = findSubPlugins(usedPlugins, flattenedPlugins);
  return render(usedPlugins, usedSubPlugins);
}

function relativePluginPath(resolve) {
  return (0, _gatsbyCoreUtils.slash)(path.relative(path.dirname(schemaCustomizationPluginsPath), resolve));
}

function render(usedPlugins, usedSubPlugins) {
  const uniqGatsbyNode = uniq(usedPlugins);
  const uniqSubPlugins = uniq(usedSubPlugins);
  const sanitizedUsedPlugins = usedPlugins.map(plugin => {
    // TODO: We don't support functions in pluginOptions here
    return { ...plugin,
      resolve: ``,
      pluginFilepath: ``,
      subPluginPaths: undefined
    };
  });
  const pluginsWithWorkers = filterPluginsWithWorkers(uniqGatsbyNode);
  const subPluginModuleToImportNameMapping = new Map();
  const imports = [...uniqGatsbyNode.map((plugin, i) => `import * as pluginGatsbyNode${i} from "gatsby/dist/schema/graphql-engine/webpack-remove-apis-loader!${relativePluginPath(plugin.resolve)}/gatsby-node"`), ...pluginsWithWorkers.map((plugin, i) => `import * as pluginGatsbyWorker${i} from "${relativePluginPath(plugin.resolve)}/gatsby-worker"`), ...uniqSubPlugins.map((plugin, i) => {
    const importName = `subPlugin${i}`;
    subPluginModuleToImportNameMapping.set(plugin.modulePath, importName);
    return `import * as ${importName} from "${relativePluginPath(plugin.modulePath)}"`;
  })];
  const gatsbyNodeExports = uniqGatsbyNode.map((plugin, i) => `"${plugin.name}": pluginGatsbyNode${i},`);
  const gatsbyWorkerExports = pluginsWithWorkers.map((plugin, i) => `"${plugin.name}": pluginGatsbyWorker${i},`);
  const output = `
${imports.join(`\n`)}

export const gatsbyNodes = {
${gatsbyNodeExports.join(`\n`)}
}

export const gatsbyWorkers = {
${gatsbyWorkerExports.join(`\n`)}
}

export const flattenedPlugins =
  ${JSON.stringify(sanitizedUsedPlugins.map(plugin => {
    return { ...plugin,
      pluginOptions: _.cloneDeepWith(plugin.pluginOptions, value => {
        if (typeof value === `object` && value !== null && value.module && value.modulePath) {
          const {
            module,
            modulePath,
            ...subPlugin
          } = value;
          return { ...subPlugin,
            module: `_SKIP_START_${subPluginModuleToImportNameMapping.get(modulePath)}_SKIP_END_`,
            resolve: ``,
            pluginFilepath: ``
          };
        }

        return undefined;
      })
    };
  }), null, 2).replace(/"_SKIP_START_|_SKIP_END_"/g, ``)}
`;
  return output;
}

function filterPluginsWithWorkers(plugins) {
  return plugins.filter(plugin => {
    try {
      return Boolean((0, _requireGatsbyPlugin.requireGatsbyPlugin)(plugin, `gatsby-worker`));
    } catch (err) {
      return false;
    }
  });
}

function getSubpluginsByPluginPath(parentPlugin, path) {
  const segments = path.split(`.`);
  let roots = [parentPlugin.pluginOptions];

  for (const segment of segments) {
    if (segment === `[]`) {
      roots = roots.flat();
    } else {
      roots = roots.map(root => root[segment]);
    }
  }

  roots = roots.flat();
  return roots;
}

function findSubPlugins(plugins, allFlattenedPlugins) {
  const usedSubPluginResolves = new Set(plugins.flatMap(plugin => {
    if (plugin.subPluginPaths) {
      const subPlugins = [];

      for (const subPluginPath of plugin.subPluginPaths) {
        subPlugins.push(...getSubpluginsByPluginPath(plugin, subPluginPath));
      }

      return subPlugins;
    }

    return [];
  }).map(plugin => plugin[`resolve`]).filter(p => typeof p === `string`));
  return allFlattenedPlugins.filter(p => usedSubPluginResolves.has(p.resolve) && !!p.modulePath);
}

function uniq(plugins) {
  return Array.from(new Map(plugins.map(p => [p.resolve, p])).values());
}
//# sourceMappingURL=print-plugins.js.map