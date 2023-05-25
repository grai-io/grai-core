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
          tableId: "1",
          n: 1,
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            graph: [
              {
                id: "2",
                name: "Table2",
                namespace: "default",
                data_source: "test",
                columns: [],
                destinations: [],
                all_destinations: [],
                all_sources: ["1"],
              },
              {
                id: "3",
                name: "Table3",
                namespace: "default",
                data_source: "test",
                columns: [],
                destinations: ["1"],
                all_destinations: ["1"],
                all_sources: [],
              },
              {
                id: "4",
                name: "Table4",
                namespace: "default",
                data_source: "test",
                columns: [],
                destinations: [],
                all_destinations: [],
                all_sources: [],
              },
            ],
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
          tableId: "1",
          n: 1,
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
          tableId: "1",
          n: 1,
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            graph: [],
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
