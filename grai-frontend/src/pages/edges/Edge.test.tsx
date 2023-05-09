import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Edge, { GET_EDGE } from "./Edge"
import { GET_TABLES_AND_EDGES } from "components/edges/EdgeLineage"

export const edgeMock = {
  request: {
    query: GET_EDGE,
    variables: {
      organisationName: "",
      workspaceName: "",
      edgeId: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        edge: {
          id: "1",
          namespace: "default",
          name: "Edge1",
          display_name: "Edge1",
          is_active: true,
          data_source: "test",
          metadata: {},
          source: {
            id: "2",
            namespace: "default",
            name: "Edge2",
            display_name: "Edge2",
          },
          destination: {
            id: "3",
            namespace: "default",
            name: "Edge3",
            display_name: "Edge3",
          },
        },
      },
    },
  },
}

const mocks = [edgeMock]

test("renders", async () => {
  render(<Edge />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Edge1")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_EDGE,
        variables: {
          organisationName: "",
          workspaceName: "",
          edgeId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Edge />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_EDGE,
        variables: {
          organisationName: "",
          workspaceName: "",
          edgeId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            edge: null,
            edges: { data: null },
            other_edges: { data: [] },
          },
        },
      },
    },
  ]

  render(<Edge />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("lineage", async () => {
  const user = userEvent.setup()

  const mocks = [
    edgeMock,
    edgeMock,
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
              ],
            },
            other_edges: { data: [] },
          },
        },
      },
    },
  ]

  render(<Edge />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Lineage")).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /Lineage/i }))
  )

  await waitFor(() => {
    expect(screen.getByTestId("edge-lineage")).toBeInTheDocument()
  })
})
