import { getEdgeTables } from "./visibleTables"

test("getEdgeTables empty", () =>
  expect(
    getEdgeTables([], {
      source: {
        id: "1",
      },
      destination: {
        id: "2",
      },
    })
  ).toEqual([]))

const table = {
  id: "1",
  columns: { data: [] },
}

test("getEdgeTables source", () =>
  expect(
    getEdgeTables([table], {
      source: {
        id: "1",
      },
      destination: {
        id: "2",
      },
    })
  ).toEqual([table]))

test("getEdgeTables destination", () =>
  expect(
    getEdgeTables([table], {
      source: {
        id: "2",
      },
      destination: {
        id: "1",
      },
    })
  ).toEqual([table]))

const columnTable = {
  id: "3",
  columns: {
    data: [
      {
        id: "1",
      },
    ],
  },
}

test("getEdgeTables column source", () =>
  expect(
    getEdgeTables([columnTable], {
      source: {
        id: "1",
      },
      destination: {
        id: "2",
      },
    })
  ).toEqual([columnTable]))

test("getEdgeTables column destination", () =>
  expect(
    getEdgeTables([columnTable], {
      source: {
        id: "2",
      },
      destination: {
        id: "1",
      },
    })
  ).toEqual([columnTable]))
