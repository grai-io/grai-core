import React from "react"
import { render, screen } from "testing"
import ColumnTests from "./ColumnTests"

test("renders empty", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: [],
  }

  render(<ColumnTests column={column} />)
})

test("renders none", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: [
      {
        id: "1",
        metadata: {
          grai: {
            edge_attributes: {},
          },
        },
        source: {
          id: "2",
          name: "source",
          display_name: "source",
          metadata: {
            grai: {
              node_attributes: {},
            },
          },
        },
      },
    ],
  }

  render(<ColumnTests column={column} />)
})

test("renders nullable", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: [
      {
        id: "1",
        metadata: {
          grai: {
            edge_attributes: {
              preserves_nullable: true,
            },
          },
        },
        source: {
          id: "2",
          name: "source",
          display_name: "source",
          metadata: {
            grai: {
              node_attributes: {
                is_nullable: false,
              },
            },
          },
        },
      },
    ],
  }

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Not Null")).toBeInTheDocument()
})

test("renders unique", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: [
      {
        id: "1",
        metadata: {
          grai: {
            edge_attributes: {
              preserves_unique: true,
            },
          },
        },
        source: {
          id: "2",
          name: "source",
          display_name: "source",
          metadata: {
            grai: {
              node_attributes: {
                is_unique: true,
              },
            },
          },
        },
      },
    ],
  }

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Unique")).toBeInTheDocument()
})

test("renders data type", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: [
      {
        id: "1",
        metadata: {
          grai: {
            edge_attributes: {
              preserves_data_type: true,
            },
          },
        },
        source: {
          id: "2",
          name: "source",
          display_name: "source",
          metadata: {
            grai: {
              node_attributes: {
                data_type: "number",
              },
            },
          },
        },
      },
    ],
  }

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Data Type: number")).toBeInTheDocument()
})
