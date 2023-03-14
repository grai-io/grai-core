import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
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
    profileMock,
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
            tables: [
              {
                id: "2",
                namespace: "default",
                name: "Table2",
                display_name: "Table2",
                data_source: "test",
                metadata: {},
                columns: [],
                source_tables: [
                  {
                    id: "1",
                    name: "Table1",
                    display_name: "Table1",
                  },
                ],
                destination_tables: [],
              },
              {
                id: "3",
                namespace: "default",
                name: "Table3",
                display_name: "Table3",
                data_source: "test",
                metadata: {},
                columns: [],
                source_tables: [],
                destination_tables: [
                  {
                    id: "1",
                    name: "Table1",
                    display_name: "Table1",
                  },
                ],
              },
              {
                id: "4",
                namespace: "default",
                name: "Table4",
                display_name: "Table4",
                data_source: "test",
                metadata: {},
                columns: [],
                source_tables: [],
                destination_tables: [],
              },
            ],
            other_edges: [],
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
    profileMock,
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
    profileMock,
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
            tables: [],
            other_edges: [],
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
