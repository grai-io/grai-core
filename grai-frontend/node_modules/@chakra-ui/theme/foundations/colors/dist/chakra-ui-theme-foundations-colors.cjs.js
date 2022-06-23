'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-theme-foundations-colors.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-theme-foundations-colors.cjs.dev.js");
}
