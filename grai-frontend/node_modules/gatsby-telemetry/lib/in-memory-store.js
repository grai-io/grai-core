"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.InMemoryConfigStore = void 0;

var _gatsbyCoreUtils = require("gatsby-core-utils");

var _os = _interopRequireDefault(require("os"));

var _path = require("path");

class InMemoryConfigStore {
  path = (0, _path.join)(_os.default.tmpdir(), `gatsby`);

  constructor() {
    this.config = this.createBaseConfig();
  }

  createBaseConfig() {
    return {
      "telemetry.enabled": true,
      "telemetry.machineId": `not-a-machine-id-${_gatsbyCoreUtils.uuid.v4()}`
    };
  }

  get(key) {
    return this.config[key];
  }

  set(key, value) {
    this.config[key] = value;
  }

  all() {
    return this.config;
  }

  size() {
    return Object.keys(this.config).length;
  }

  has(key) {
    return !!this.config[key];
  }

  delete(key) {
    delete this.config[key];
  }

  clear() {
    this.config = this.createBaseConfig();
  }

}

exports.InMemoryConfigStore = InMemoryConfigStore;