'use strict';

if (process.env.NODE_ENV === "production") {
  module.exports = require("./chakra-ui-hooks-use-animation-state.cjs.prod.js");
} else {
  module.exports = require("./chakra-ui-hooks-use-animation-state.cjs.dev.js");
}
