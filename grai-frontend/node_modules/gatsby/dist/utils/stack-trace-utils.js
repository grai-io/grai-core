"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

exports.__esModule = true;
exports.findOriginalSourcePositionAndContent = findOriginalSourcePositionAndContent;
exports.getNonGatsbyCodeFrameFormatted = exports.getNonGatsbyCodeFrame = void 0;

var _stackTrace = _interopRequireDefault(require("stack-trace"));

var _codeFrame = require("@babel/code-frame");

var _sourceMap = require("source-map");

const fs = require(`fs-extra`);

const path = require(`path`);

const chalk = require(`chalk`);

const {
  isNodeInternalModulePath
} = require(`gatsby-core-utils`);

const getDirName = arg => {
  // Caveat related to executing in engines:
  // After webpack bundling we would get number here (webpack module id) and that would crash when doing
  // path.dirname(number).
  if (typeof arg === `string`) {
    return path.dirname(arg);
  }

  return `-cant-resolve-`;
};

const gatsbyLocation = getDirName(require.resolve(`gatsby/package.json`));
const reduxThunkLocation = getDirName(require.resolve(`redux-thunk/package.json`));
const reduxLocation = getDirName(require.resolve(`redux/package.json`));

const getNonGatsbyCallSite = () => _stackTrace.default.get().find(callSite => callSite && callSite.getFileName() && !callSite.getFileName().includes(gatsbyLocation) && !callSite.getFileName().includes(reduxLocation) && !callSite.getFileName().includes(reduxThunkLocation) && !isNodeInternalModulePath(callSite.getFileName()));

const getNonGatsbyCodeFrame = ({
  highlightCode = true,
  stack
} = {}) => {
  let callSite;

  if (stack) {
    callSite = _stackTrace.default.parse({
      stack,
      name: ``,
      message: ``
    })[0];
  } else {
    callSite = getNonGatsbyCallSite();
  }

  if (!callSite) {
    return null;
  }

  const fileName = callSite.getFileName();
  const line = callSite.getLineNumber();
  const column = callSite.getColumnNumber();
  const code = fs.readFileSync(fileName, {
    encoding: `utf-8`
  });
  return {
    fileName,
    line,
    column,
    codeFrame: (0, _codeFrame.codeFrameColumns)(code, {
      start: {
        line,
        column
      }
    }, {
      highlightCode
    })
  };
};

exports.getNonGatsbyCodeFrame = getNonGatsbyCodeFrame;

const getNonGatsbyCodeFrameFormatted = ({
  highlightCode = true,
  stack
} = {}) => {
  const possibleCodeFrame = getNonGatsbyCodeFrame({
    highlightCode,
    stack
  });

  if (!possibleCodeFrame) {
    return null;
  }

  const {
    fileName,
    line,
    column,
    codeFrame
  } = possibleCodeFrame;
  return `File ${chalk.bold(`${fileName}:${line}:${column}`)}\n${codeFrame}`;
};

exports.getNonGatsbyCodeFrameFormatted = getNonGatsbyCodeFrameFormatted;

async function findOriginalSourcePositionAndContent(webpackSource, position) {
  return await _sourceMap.SourceMapConsumer.with(webpackSource, null, consumer => {
    var _position$column, _consumer$sourceConte;

    const sourcePosition = consumer.originalPositionFor({
      line: position.line,
      column: (_position$column = position.column) !== null && _position$column !== void 0 ? _position$column : 0
    });

    if (!sourcePosition.source) {
      return {
        sourcePosition: null,
        sourceContent: null
      };
    }

    const sourceContent = (_consumer$sourceConte = consumer.sourceContentFor(sourcePosition.source, true)) !== null && _consumer$sourceConte !== void 0 ? _consumer$sourceConte : null;
    return {
      sourcePosition,
      sourceContent
    };
  });
}
//# sourceMappingURL=stack-trace-utils.js.map