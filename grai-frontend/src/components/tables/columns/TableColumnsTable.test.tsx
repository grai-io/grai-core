import React from "react"
import { render, screen } from "testing"
import TableColumnsTable, { Column } from "./TableColumnsTable"

const columns: Column[] = [
  {
    id: "1",
    name: "col1",
    display_name: "Column 1",
    metadata: null,
  },
]

test("renders", async () => {
  render(<TableColumnsTable search={null} columns={columns} />)

  expect(screen.getByText("Column 1")).toBeInTheDocument()
})

test("empty", async () => {
  render(<TableColumnsTable search={null} columns={[]} />)

  expect(screen.getByText("No columns found")).toBeInTheDocument()
  expect(screen.queryByText("Try clearing search")).toBeFalsy()
})

test("search", async () => {
  render(<TableColumnsTable search="search" columns={columns} />)

  expect(screen.getByText("No columns found")).toBeInTheDocument()
  expect(screen.getByText("Try clearing search")).toBeInTheDocument()
})
