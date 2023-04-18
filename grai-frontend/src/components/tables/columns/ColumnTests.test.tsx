import React from "react"
import { enrichColumn } from "helpers/columns"
import { render, screen } from "testing"
import ColumnTests from "./ColumnTests"

test("renders empty", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: { data: [] },
  })

  render(<ColumnTests column={column} />)
})

test("renders none", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: {
      data: [
        {
          metadata: {
            grai: {
              edge_attributes: {},
            },
          },
          destination: {
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
    },
  })

  render(<ColumnTests column={column} />)
})

test("renders nullable", async () => {
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
    requirements_edges: {
      data: [
        {
          metadata: {
            grai: {
              edge_attributes: {
                preserves_nullable: true,
              },
            },
          },
          destination: {
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
    },
  })

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Not Null")).toBeInTheDocument()
})

test("renders unique", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: {
      data: [
        {
          metadata: {
            grai: {
              edge_attributes: {
                preserves_unique: true,
              },
            },
          },
          destination: {
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
    },
  })

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Unique")).toBeInTheDocument()
})

test("renders data type", async () => {
  const column = enrichColumn({
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: {
      data: [
        {
          metadata: {
            grai: {
              edge_attributes: {
                preserves_data_type: true,
              },
            },
          },
          destination: {
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
    },
  })

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Data Type: number")).toBeInTheDocument()
})

test("renders repeated", async () => {
  const column = {
    id: "1",
    name: "column",
    display_name: "column",
    metadata: null,
    requirements_edges: { data: [] },
    tests: [
      {
        text: "Unique",
        passed: true,
        type: "unique",
        destination: {
          name: "s1",
          display_name: "s1",
        },
      },
      {
        text: "Unique",
        passed: true,
        type: "unique",
        destination: {
          name: "s2",
          display_name: "s2",
        },
      },
    ],
    properties: [],
    requirements: [],
  }

  render(<ColumnTests column={column} />)

  expect(screen.getByText("Unique")).toBeInTheDocument()
})
