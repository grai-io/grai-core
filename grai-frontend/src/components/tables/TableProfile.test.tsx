import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import TableProfile from "./TableProfile"

const other_table = {
  id: "2",
  display_name: "other table",
}

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
  sourceTables: [other_table],
  destinationTables: [other_table],
}

test("renders", async () => {
  renderWithRouter(<TableProfile table={table} />)

  await waitFor(() => {
    expect(screen.getByText("Table 1")).toBeInTheDocument()
  })
})
