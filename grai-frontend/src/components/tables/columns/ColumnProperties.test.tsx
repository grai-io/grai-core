import React from "react"
import { enrichColumn } from "helpers/columns"
import { render, screen } from "testing"
import ColumnProperties from "./ColumnProperties"

test("renders", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: [],
  })

  render(<ColumnProperties column={column} />)
})

test("renders empty", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: {
      grai: {
        node_attributes: {},
      },
    },
    requirements_edges: [],
  })

  render(<ColumnProperties column={column} />)
})

test("renders not null", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: {
      grai: {
        node_attributes: {
          is_nullable: false,
        },
      },
    },
    requirements_edges: [],
  })

  render(<ColumnProperties column={column} />)

  expect(screen.getByText("Not Null")).toBeInTheDocument()
})

test("renders unique", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: {
      grai: {
        node_attributes: {
          is_unique: true,
        },
      },
    },
    requirements_edges: [],
  })

  render(<ColumnProperties column={column} />)

  expect(screen.getByText("Unique")).toBeInTheDocument()
})

test("renders primary key", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: {
      grai: {
        node_attributes: {
          is_primary_key: true,
        },
      },
    },
    requirements_edges: [],
  })

  render(<ColumnProperties column={column} />)

  expect(screen.getByText("Primary Key")).toBeInTheDocument()
})
