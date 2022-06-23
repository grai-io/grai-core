'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-theme-foundations-z-index.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-theme-foundations-z-index.cjs.dev.js");
}
