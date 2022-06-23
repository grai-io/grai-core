/**
 * @module utils
 * @description provided utility function.
 */
const {
  pascalCase,
  camelCase,
  snakeCase,
  constantCase,
} = require("change-case");

/**
 * @memberof utils
 * @name compose
 * @param {Array}
 * @return {T}
 */
const compose =
  (...args) =>
  (x) =>
    [...args].reduce((_x, fn) => fn(_x), x);
/**
 * @memberof utils
 * @name pairToObject
 * @param {Array}
 * @returns {Object}
 */
const pairToObject = ([key, value]) => ({ [key]: value });
/**
 * @memberof utils
 * @name objectToPair
 * @param {Object}
 * @returns {Array}
 */
const objectToPair = (object) => objectToPairs(object)[0];
/**
 * @memberof utils
 * @name pairsToObject
 * @param {[String,Any][]} pairs
 * @returns {Object}
 * @example
 * const pairs = [
 *  ["name", "ninja"],
 *  ["from", "japan"],
 * ];
 *
 * const ninjaObject = pairsToObject(pairs)
 * // {
 * // name: "ninja",
 * // from: "japan",
 * // }
 */
const pairsToObject = (pairs) => Object.fromEntries(pairs);
/**
 * @memberof utils
 * @name objectToPairs
 * @param {Object}
 * @returns {Array}
 */
const objectToPairs = (object) => Object.entries(object);
/**
 *
 * @memberof utils
 * @name stringToCase
 * @param {String} str
 * @param {String} [_case="pascal"] - case style "camel" | "constant" | "snake"
 * @returns {String}
 * @example
 * const str = "Hei"
 * stringToCase(str, "constant")
 * // HEI
 */
const stringToCase = (str, _case) =>
  ({
    [true]: pascalCase(str),
    [_case === "camel"]: camelCase(str),
    [_case === "constant"]: constantCase(str),
    [_case === "snake"]: snakeCase(str),
  }[true]);

module.exports = {
  pairToObject,
  objectToPair,
  pairsToObject,
  objectToPairs,
  compose,
  stringToCase,
};
