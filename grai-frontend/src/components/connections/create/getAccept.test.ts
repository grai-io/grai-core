import getAccept from "./getAccept"

test("json", () => {
  expect(getAccept("json")).toEqual({
    "application/json": [".json"],
  })
})

test("yaml", () => {
  expect(getAccept("yaml")).toEqual({
    "application/yaml": [".yaml", ".yml"],
  })
})

test("flat-file", () => {
  expect(getAccept("flat-file")).toEqual({
    "application/octet-stream": [".csv", ".parquet", ".feather", ".arrow"],
  })
})

test("other", () => {
  expect(getAccept("other")).toEqual({
    "*": ["*"],
  })
})
