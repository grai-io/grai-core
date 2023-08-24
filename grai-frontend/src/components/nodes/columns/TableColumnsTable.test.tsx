import React from "react"
import { render, screen } from "testing"
import TableColumnsTable, { Column } from "./TableColumnsTable"

const columns: Column[] = [
  {
    id: "1",
    name: "col1",
    display_name: "Column 1",
    metadata: null,
    requirements_edges: {
      data: [
        {
          metadata: null,
          destination: {
            id: "1",
            name: "col2",
            display_name: "Column 2",
            metadata: {
              grai: null,
            },
          },
        },
      ],
    },
  },
]

test("renders", async () => {
  render(
    <TableColumnsTable
      search={null}
      columns={columns}
      expanded={[]}
      onExpand={() => {}}
    />,
    {
      withRouter: true,
    },
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
    />,
    {
      withRouter: true,
    },
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
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText("No columns found")).toBeInTheDocument()
  expect(screen.getByText("Try clearing search")).toBeInTheDocument()
})

test("expanded", async () => {
  render(
    <TableColumnsTable
      search={null}
      columns={columns}
      expanded={["1"]}
      onExpand={() => {}}
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText("Column 1")).toBeInTheDocument()
  expect(screen.getByText("col2")).toBeInTheDocument()
})
