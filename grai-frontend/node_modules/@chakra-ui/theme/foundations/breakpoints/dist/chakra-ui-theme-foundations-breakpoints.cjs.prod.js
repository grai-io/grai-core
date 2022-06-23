'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var themeTools = require('@chakra-ui/theme-tools');

/**
 * Breakpoints for responsive design
 */

var breakpoints = themeTools.createBreakpoints({
  sm: "30em",
  md: "48em",
  lg: "62em",
  xl: "80em",
  "2xl": "96em"
});

exports["default"] = breakpoints;
