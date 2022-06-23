"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.createModel = void 0;
var actions_1 = require("./actions");
var Machine_1 = require("./Machine");
var utils_1 = require("./utils");
function createModel(initialContext, creators) {
    var eventCreators = creators === null || creators === void 0 ? void 0 : creators.events;
    var actionCreators = creators === null || creators === void 0 ? void 0 : creators.actions;
    var model = {
        initialContext: initialContext,
        assign: actions_1.assign,
        events: (eventCreators
            ? (0, utils_1.mapValues)(eventCreators, function (fn, eventType) { return function () {
                var args = [];
                for (var _i = 0; _i < arguments.length; _i++) {
                    args[_i] = arguments[_i];
                }
                return (__assign(__assign({}, fn.apply(void 0, __spreadArray([], __read(args), false))), { type: eventType }));
            }; })
            : undefined),
        actions: actionCreators
            ? (0, utils_1.mapValues)(actionCreators, function (fn, actionType) { return function () {
                var args = [];
                for (var _i = 0; _i < arguments.length; _i++) {
                    args[_i] = arguments[_i];
                }
                return (__assign(__assign({}, fn.apply(void 0, __spreadArray([], __read(args), false))), { type: actionType }));
            }; })
            : undefined,
        reset: function () { return (0, actions_1.assign)(initialContext); },
        createMachine: function (config, implementations) {
            return (0, Machine_1.createMachine)('context' in config ? config : __assign(__assign({}, config), { context: initialContext }), implementations);
        }
    };
    return model;
}
exports.createModel = createModel;
