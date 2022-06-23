'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-theme-foundations-spacing.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-theme-foundations-spacing.cjs.dev.js");
}
