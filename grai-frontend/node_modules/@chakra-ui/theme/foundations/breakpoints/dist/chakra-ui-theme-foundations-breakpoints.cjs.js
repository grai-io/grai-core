'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-theme-foundations-breakpoints.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-theme-foundations-breakpoints.cjs.dev.js");
}
