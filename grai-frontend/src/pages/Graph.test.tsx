import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Graph, { GET_NODES_AND_EDGES } from "./Graph"

test("renders", async () => {
  window.ResizeObserver = jest.fn().mockImplementation(() => ({
    disconnect: jest.fn(),
    observe: jest.fn(),
    unobserve: jest.fn(),
  }))

  renderWithRouter(<Graph />)

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })
})

test("renders with errors", async () => {
  window.ResizeObserver = jest.fn().mockImplementation(() => ({
    disconnect: jest.fn(),
    observe: jest.fn(),
    unobserve: jest.fn(),
  }))

  renderWithRouter(<Graph />, {
    path: "/workspaces/:workspaceId/graph",
    route:
      "/workspaces/1234/graph?errors=%5B%7B%22source%22%3A%20%22a%22%2C%20%22destination%22%3A%20%22b%22%2C%20%22test%22%3A%20%22nullable%22%2C%20%22message%22%3A%20%22not%20null%22%7D%5D",
  })

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })
})

test("renders with limitGraph", async () => {
  window.ResizeObserver = jest.fn().mockImplementation(() => ({
    disconnect: jest.fn(),
    observe: jest.fn(),
    unobserve: jest.fn(),
  }))

  renderWithRouter(<Graph />, {
    path: "/workspaces/:workspaceId/graph",
    route: "/workspaces/1234/graph?limitGraph=true",
  })

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_NODES_AND_EDGES,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Graph />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})

test("no nodes", async () => {
  const mock = {
    request: {
      query: GET_NODES_AND_EDGES,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          nodes: null,
          edges: null,
        },
      },
    },
  }

  renderWithMocks(<Graph />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("No nodes found")).toBeTruthy()
  })
})
