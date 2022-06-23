'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-theme-foundations-sizes.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-theme-foundations-sizes.cjs.dev.js");
}
