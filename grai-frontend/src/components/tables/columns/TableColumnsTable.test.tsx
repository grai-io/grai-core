import React from "react"
import { render, screen } from "testing"
import TableColumnsTable, { Column } from "./TableColumnsTable"

const columns: Column[] = [
  {
    id: "1",
    name: "col1",
    display_name: "Column 1",
    metadata: null,
    requirements_edges: [],
  },
]

test("renders", async () => {
  render(
    <TableColumnsTable
      search={null}
      columns={columns}
      expanded={[]}
      onExpand={() => {}}
    />
  )

  expect(screen.getByText("Column 1")).toBeInTheDocument()
})

test("empty", async () => {
  render(
    <TableColumnsTable
      search={null}
      columns={[]}
      expanded={[]}
      onExpand={() => {}}
    />
  )

  expect(screen.getByText("No columns found")).toBeInTheDocument()
  expect(screen.queryByText("Try clearing search")).toBeFalsy()
})

test("search", async () => {
  render(
    <TableColumnsTable
      search="search"
      columns={columns}
      expanded={[]}
      onExpand={() => {}}
    />
  )

  expect(screen.getByText("No columns found")).toBeInTheDocument()
  expect(screen.getByText("Try clearing search")).toBeInTheDocument()
})
