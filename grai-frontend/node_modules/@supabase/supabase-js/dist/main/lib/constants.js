"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.STORAGE_KEY = exports.DEFAULT_HEADERS = void 0;
// constants.ts
const version_1 = require("./version");
exports.DEFAULT_HEADERS = { 'X-Client-Info': `supabase-js/${version_1.version}` };
exports.STORAGE_KEY = 'supabase.auth.token';
//# sourceMappingURL=constants.js.map