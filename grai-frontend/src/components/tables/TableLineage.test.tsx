import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import { tableMock } from "pages/tables/Table.test"
import TableLineage, {
  GET_TABLES_AND_EDGES,
} from "components/tables/TableLineage"

const table = {
  id: "1",
  display_name: "Table 1",
}

test("renders", async () => {
  const mocks = [
    tableMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            tables: {
              data: [
                {
                  id: "2",
                  namespace: "default",
                  name: "Table2",
                  display_name: "Table2",
                  data_source: "test",
                  metadata: {},
                  columns: { data: [] },
                  source_tables: {
                    data: [
                      {
                        id: "1",
                        name: "Table1",
                        display_name: "Table1",
                      },
                    ],
                  },
                  destination_tables: { data: [] },
                },
                {
                  id: "3",
                  namespace: "default",
                  name: "Table3",
                  display_name: "Table3",
                  data_source: "test",
                  metadata: {},
                  columns: { data: [] },
                  source_tables: { data: [] },
                  destination_tables: {
                    data: [
                      {
                        id: "1",
                        name: "Table1",
                        display_name: "Table1",
                      },
                    ],
                  },
                },
                {
                  id: "4",
                  namespace: "default",
                  name: "Table4",
                  display_name: "Table4",
                  data_source: "test",
                  metadata: {},
                  columns: { data: [] },
                  source_tables: { data: [] },
                  destination_tables: { data: [] },
                },
              ],
            },
            other_edges: { data: [] },
          },
        },
      },
    },
  ]

  render(<TableLineage table={table} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByTestId("table-lineage")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    tableMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<TableLineage table={table} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no tables", async () => {
  const mocks = [
    tableMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            tables: { data: null },
            other_edges: { data: [] },
          },
        },
      },
    },
  ]

  render(<TableLineage table={table} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})
