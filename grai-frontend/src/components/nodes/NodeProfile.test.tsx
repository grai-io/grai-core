import { render, screen, waitFor } from "testing"
import NodeProfile from "./NodeProfile"

const other_table = {
  id: "2",
  display_name: "other table",
}

test("renders", async () => {
  const table = {
    id: "1",
    name: "Table 1",
    namespace: "default",
    display_name: "Table 1",
    columns: { data: [] },
    metadata: {
      grai: {
        node_type: "Table",
      },
    },
    source_tables: { data: [other_table] },
    destination_tables: { data: [other_table] },
    data_sources: {
      data: [
        {
          id: "1",
          name: "source 1",
        },
      ],
    },
  }

  render(<NodeProfile node={table} />, {
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
    display_name: "Table 1",
    columns: { data: [] },
    metadata: {
      grai: {
        node_type: "Table",
      },
    },
    source_tables: { data: [] },
    destination_tables: { data: [] },
    data_sources: {
      data: [],
    },
  }

  render(<NodeProfile node={table} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Table 1")).toBeInTheDocument()
  })
})
