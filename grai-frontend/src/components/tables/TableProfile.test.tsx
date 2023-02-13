import React from "react"
import { render, screen, waitFor } from "testing"
import TableProfile from "./TableProfile"

const other_table = {
  id: "2",
  display_name: "other table",
}

test("renders", async () => {
  const table = {
    id: "1",
    name: "Table 1",
    namespace: "default",
    data_source: "test-source",
    display_name: "Table 1",
    columns: [],
    metadata: {
      grai: {
        node_type: "Table",
      },
    },
    source_tables: [other_table],
    destination_tables: [other_table],
  }

  render(<TableProfile table={table} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Table 1")).toBeInTheDocument()
  })
})

test("renders no sources or destinations", async () => {
  const table = {
    id: "1",
    name: "Table 1",
    namespace: "default",
    data_source: "test-source",
    display_name: "Table 1",
    columns: [],
    metadata: {
      grai: {
        node_type: "Table",
      },
    },
    source_tables: [],
    destination_tables: [],
  }

  render(<TableProfile table={table} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Table 1")).toBeInTheDocument()
  })
})
