"use strict";

exports.__esModule = true;
exports.default = copyFunctionsManifest;

var _fsExtra = require("fs-extra");

var _constants = require("./constants");

async function copyFunctionsManifest(pluginData) {
  const {
    publicFolder,
    functionsFolder
  } = pluginData;
  const manifestPath = functionsFolder(_constants.CACHE_FUNCTIONS_FILENAME);
  const publicManifestPath = publicFolder(_constants.PUBLIC_FUNCTIONS_FILENAME);
  const hasManifestFile = (0, _fsExtra.existsSync)(manifestPath);

  if (hasManifestFile) {
    await (0, _fsExtra.copyFile)(manifestPath, publicManifestPath);
  }
}