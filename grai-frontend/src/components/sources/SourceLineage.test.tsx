import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import { filtersMock } from "pages/Graph.test"
import { tableMock } from "pages/nodes/Node.test"
import SourceLineage, { GET_TABLES_AND_EDGES } from "./SourceLineage"

const source = {
  id: "1",
}

test("renders", async () => {
  const mocks = [
    tableMock,
    filtersMock,
    filtersMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          sourceId: "1",
          n: 0,
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
                display_name: "Table2",
                namespace: "default",
                data_source: "test",
                x: 0,
                y: 0,
                columns: [],
                destinations: [],
                table_destinations: [],
                table_sources: ["1"],
              },
              {
                id: "3",
                name: "Table3",
                display_name: "Table3",
                namespace: "default",
                data_source: "test",
                x: 0,
                y: 0,
                columns: [],
                destinations: [{ table_id: "1", edge_id: "1" }],
                table_destinations: ["1"],
                table_sources: [],
              },
              {
                id: "4",
                name: "Table4",
                display_name: "Table4",
                namespace: "default",
                data_source: "test",
                x: 0,
                y: 0,
                columns: [],
                destinations: [],
                table_destinations: [],
                table_sources: [],
              },
            ],
          },
        },
      },
    },
  ]

  render(<SourceLineage source={source} />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByTestId("source-lineage")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    tableMock,
    filtersMock,
    filtersMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          sourceId: "1",
          n: 0,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<SourceLineage source={source} />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no tables", async () => {
  const mocks = [
    tableMock,
    filtersMock,
    filtersMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          sourceId: "1",
          n: 0,
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

  render(<SourceLineage source={source} />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})
