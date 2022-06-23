"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.GatsbyWebpackStatsExtractor = void 0;

var _fsExtra = _interopRequireDefault(require("fs-extra"));

var _path = _interopRequireDefault(require("path"));

class GatsbyWebpackStatsExtractor {
  constructor() {
    this.plugin = {
      name: `GatsbyWebpackStatsExtractor`
    };
  }

  apply(compiler) {
    let previousChunkMapJson;
    let previousWebpackStatsJson;
    compiler.hooks.done.tapAsync(this.plugin.name, async (stats, done) => {
      const assets = {};
      const assetsMap = {};
      const childAssets = {};

      for (const chunkGroup of stats.compilation.chunkGroups) {
        if (chunkGroup.name) {
          const files = [];

          for (const chunk of chunkGroup.chunks) {
            files.push(...chunk.files);
          }

          assets[chunkGroup.name] = files.filter(f => f.slice(-4) !== `.map`);
          assetsMap[chunkGroup.name] = files.filter(f => {
            var _chunkGroup$name;

            return f.slice(-4) !== `.map` && f.slice(0, (_chunkGroup$name = chunkGroup.name) === null || _chunkGroup$name === void 0 ? void 0 : _chunkGroup$name.length) === chunkGroup.name;
          }).map(filename => `/${filename}`);

          for (const [rel, childChunkGroups] of Object.entries(chunkGroup.getChildrenByOrders(stats.compilation.moduleGraph, stats.compilation.chunkGraph))) {
            if (!(chunkGroup.name in childAssets)) {
              childAssets[chunkGroup.name] = {};
            }

            const childFiles = [];

            for (const childChunkGroup of childChunkGroups) {
              for (const chunk of childChunkGroup.chunks) {
                childFiles.push(...chunk.files);
              }
            }

            childAssets[chunkGroup.name][rel] = childFiles;
          }
        }
      }

      const webpackStats = { ...stats.toJson({
          all: false,
          chunkGroups: true
        }),
        assetsByChunkName: assets,
        childAssetsByChunkName: childAssets
      };
      const newChunkMapJson = JSON.stringify(assetsMap);

      if (newChunkMapJson !== previousChunkMapJson) {
        await _fsExtra.default.writeFile(_path.default.join(`public`, `chunk-map.json`), newChunkMapJson);
        previousChunkMapJson = newChunkMapJson;
      }

      const newWebpackStatsJson = JSON.stringify(webpackStats);

      if (newWebpackStatsJson !== previousWebpackStatsJson) {
        await _fsExtra.default.writeFile(_path.default.join(`public`, `webpack.stats.json`), newWebpackStatsJson);
        previousWebpackStatsJson = newWebpackStatsJson;
      }

      done();
    });
  }

}

exports.GatsbyWebpackStatsExtractor = GatsbyWebpackStatsExtractor;
//# sourceMappingURL=gatsby-webpack-stats-extractor.js.map