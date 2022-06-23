"use strict";

exports.__esModule = true;
exports.shouldPrintEngineSnapshot = shouldPrintEngineSnapshot;
exports.shouldGenerateEngines = shouldGenerateEngines;

var _redux = require("../redux");

function shouldPrintEngineSnapshot() {
  return process.env.gatsby_executing_command === `build`;
}

let generate = false;

function shouldGenerateEngines() {
  return process.env.gatsby_executing_command === `build` && generate;
}

_redux.emitter.on(`CREATE_PAGE`, action => {
  if (action.payload.mode && action.payload.mode !== `SSG`) generate = true;
});

_redux.emitter.on(`SET_COMPONENT_FEATURES`, action => {
  if (action.payload.serverData) generate = true;
  if (action.payload.config) generate = true;
});
//# sourceMappingURL=engines-helpers.js.map