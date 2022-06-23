"use strict";

exports.__esModule = true;
exports.validateEngines = validateEngines;

var _gatsbyWorker = require("gatsby-worker");

async function validateEngines(directory) {
  const worker = new _gatsbyWorker.WorkerPool(require.resolve(`./child`), {
    numWorkers: 1,
    env: {
      // Do not "inherit" this env var for validation,
      // as otherwise validation will fail on any imports
      // that OpenTracing config might make
      GATSBY_OPEN_TRACING_CONFIG_FILE: ``
    },
    silent: true
  });

  try {
    await worker.single.validate(directory);
  } finally {
    worker.end();
  }
}
//# sourceMappingURL=index.js.map