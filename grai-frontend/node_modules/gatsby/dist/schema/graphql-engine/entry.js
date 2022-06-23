"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.default = exports.GraphQLEngine = void 0;

require("../../utils/engines-fs-provider");

var _gatsbyCoreUtils = require("gatsby-core-utils");

var _index = require("../index");

var _lmdbDatastore = require("../../datastore/lmdb/lmdb-datastore");

var _redux = require("../../redux");

var _actions = require("../../redux/actions");

var _reporter = _interopRequireDefault(require("gatsby-cli/lib/reporter"));

var _graphqlRunner = require("../../query/graphql-runner");

var _waitUntilJobsComplete = require("../../utils/wait-until-jobs-complete");

var _requireGatsbyPlugin = require("../../utils/require-gatsby-plugin");

var _apiRunnerNode = _interopRequireDefault(require("../../utils/api-runner-node"));

var _findPageByPath = require("../../utils/find-page-by-path");

var _engineContext = require("../../utils/engine-context");

var _datastore = require("../../datastore");

var _queryEnginePlugins = require(".cache/query-engine-plugins");

var _tracer = require("../../utils/tracer");

var _process$env$GATSBY_O;

const tracerReadyPromise = (0, _tracer.initTracer)((_process$env$GATSBY_O = process.env.GATSBY_OPEN_TRACING_CONFIG_FILE) !== null && _process$env$GATSBY_O !== void 0 ? _process$env$GATSBY_O : ``);

class GraphQLEngine {
  // private schema: GraphQLSchema
  constructor({
    dbPath
  }) {
    (0, _lmdbDatastore.setupLmdbStore)({
      dbPath
    }); // start initializing runner ASAP

    this.getRunner();
  }

  async _doGetRunner() {
    await tracerReadyPromise;

    const wrapActivity = _reporter.default.phantomActivity(`Initializing GraphQL Engine`);

    wrapActivity.start();

    try {
      // @ts-ignore SCHEMA_SNAPSHOT is being "inlined" by bundler
      _redux.store.dispatch(_actions.actions.createTypes(SCHEMA_SNAPSHOT)); // TODO: FLATTENED_PLUGINS needs to be merged with plugin options from gatsby-config
      //  (as there might be non-serializable options, i.e. functions)


      _redux.store.dispatch({
        type: `SET_SITE_FLATTENED_PLUGINS`,
        payload: _queryEnginePlugins.flattenedPlugins
      });

      for (const pluginName of Object.keys(_queryEnginePlugins.gatsbyNodes)) {
        (0, _requireGatsbyPlugin.setGatsbyPluginCache)({
          name: pluginName,
          resolve: ``
        }, `gatsby-node`, _queryEnginePlugins.gatsbyNodes[pluginName]);
      }

      for (const pluginName of Object.keys(_queryEnginePlugins.gatsbyWorkers)) {
        (0, _requireGatsbyPlugin.setGatsbyPluginCache)({
          name: pluginName,
          resolve: ``
        }, `gatsby-worker`, _queryEnginePlugins.gatsbyWorkers[pluginName]);
      }

      if ("4" === `4`) {
        await (0, _apiRunnerNode.default)(`onPluginInit`, {
          parentSpan: wrapActivity.span
        });
      } else {
        await (0, _apiRunnerNode.default)(`unstable_onPluginInit`, {
          parentSpan: wrapActivity.span
        });
      }

      await (0, _apiRunnerNode.default)(`createSchemaCustomization`, {
        parentSpan: wrapActivity.span
      }); // Build runs
      // Note: skipping inference metadata because we rely on schema snapshot

      await (0, _index.build)({
        fullMetadataBuild: false,
        parentSpan: wrapActivity.span
      });
      return new _graphqlRunner.GraphQLRunner(_redux.store);
    } finally {
      wrapActivity.end();
    }
  }

  async getRunner() {
    if (!this.runnerPromise) {
      this.runnerPromise = this._doGetRunner();
    }

    return this.runnerPromise;
  }

  async ready() {
    // We don't want to expose internal runner freely. We do expose `runQuery` function already.
    // The way internal runner works can change, so we should not make it a public API.
    // Here we just want to expose way to await it being ready
    await this.getRunner();
  }

  async runQuery(query, context = {}, opts) {
    const engineContext = {
      requestId: _gatsbyCoreUtils.uuid.v4()
    };

    const doRunQuery = async () => {
      if (!opts) {
        opts = {
          queryName: `GraphQL Engine query`,
          parentSpan: undefined
        };
      }

      let gettingRunnerActivity;
      let graphqlRunner;

      try {
        if (opts.parentSpan) {
          gettingRunnerActivity = _reporter.default.phantomActivity(`Waiting for graphql runner to init`, {
            parentSpan: opts.parentSpan
          });
          gettingRunnerActivity.start();
        }

        graphqlRunner = await this.getRunner();
      } finally {
        if (gettingRunnerActivity) {
          gettingRunnerActivity.end();
        }
      } // graphqlRunner creates it's own Span as long as we pass `parentSpan`


      const result = await graphqlRunner.query(query, context, opts);
      let waitingForJobsCreatedByCurrentRequestActivity;

      try {
        if (opts.parentSpan) {
          waitingForJobsCreatedByCurrentRequestActivity = _reporter.default.phantomActivity(`Waiting for jobs to finish`, {
            parentSpan: opts.parentSpan
          });
          waitingForJobsCreatedByCurrentRequestActivity.start();
        }

        await (0, _waitUntilJobsComplete.waitJobsByRequest)(engineContext.requestId);
      } finally {
        if (waitingForJobsCreatedByCurrentRequestActivity) {
          waitingForJobsCreatedByCurrentRequestActivity.end();
        }
      }

      return result;
    };

    try {
      return await (0, _engineContext.runWithEngineContext)(engineContext, doRunQuery);
    } finally {
      // Reset job-to-request mapping
      _redux.store.dispatch({
        type: `CLEAR_JOB_V2_CONTEXT`,
        payload: engineContext
      });
    }
  }

  findPageByPath(pathName) {
    // adapter so `findPageByPath` use SitePage nodes in datastore
    // instead of `pages` redux slice
    const state = {
      pages: {
        get(pathName) {
          return (0, _datastore.getDataStore)().getNode(`SitePage ${pathName}`);
        },

        values() {
          return (0, _datastore.getDataStore)().iterateNodesByType(`SitePage`);
        }

      }
    };
    return (0, _findPageByPath.findPageByPath)(state, pathName, false);
  }

}

exports.GraphQLEngine = GraphQLEngine;
var _default = {
  GraphQLEngine
};
exports.default = _default;
//# sourceMappingURL=entry.js.map