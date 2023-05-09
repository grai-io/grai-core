import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Edge, { GET_EDGE } from "./Edge"

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
    expect(screen.getByText("Edge1")).toBeInTheDocument()
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
