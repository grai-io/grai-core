import React from "react"
import { render, screen } from "testing"
import ColumnConstraints from "./ColumnConstraints"

test("renders", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
  }

  render(<ColumnConstraints column={column} />)
})

test("renders empty", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: {
      grai: {
        node_attributes: {},
      },
    },
  }

  render(<ColumnConstraints column={column} />)
})

test("renders not null", async () => {
  const column = {
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
  }

  render(<ColumnConstraints column={column} />)

  expect(screen.getByText("Not Null")).toBeInTheDocument()
})

test("renders unique", async () => {
  const column = {
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
  }

  render(<ColumnConstraints column={column} />)

  expect(screen.getByText("Unique")).toBeInTheDocument()
})

test("renders primary key", async () => {
  const column = {
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
  }

  render(<ColumnConstraints column={column} />)

  expect(screen.getByText("Primary Key")).toBeInTheDocument()
})
