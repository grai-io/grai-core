'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-theme-components.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-theme-components.cjs.dev.js");
}
