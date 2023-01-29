import valueToString from "./valueToString"

test("valueToString_string", () =>
  expect(valueToString("string value")).toEqual("string value"))

test("valueToString_boolean_true", () =>
  expect(valueToString(true)).toEqual("yes"))

test("valueToString_boolean_false", () =>
  expect(valueToString(false)).toEqual("no"))

const object = {
  a: 1,
  b: "b",
  c: true,
  d: null,
}

test("valueToString_object", () =>
  expect(valueToString(object)).toEqual(JSON.stringify(object)))
