import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Graph, { GET_TABLES_AND_EDGES } from "./Graph"

const sourceNode = {
  id: "1",
  namespace: "default",
  name: "N1",
  display_name: "N1",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
}

const destinationNode = {
  id: "2",
  namespace: "default",
  name: "N2",
  display_name: "N2 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
}

const columnNode = {
  id: "3",
  namespace: "default",
  name: "N3",
  display_name: "N3 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Column",
    },
  },
}

const mock = {
  request: {
    query: GET_TABLES_AND_EDGES,
    variables: {
      workspaceId: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        tables: [sourceNode, destinationNode, columnNode],
        other_edges: [
          {
            id: "1",
            is_active: true,
            data_source: "test",
            source: sourceNode,
            destination: destinationNode,
            metadata: { grai: { constraint_type: "dbt_model" } },
          },
          {
            id: "2",
            is_active: true,
            data_source: "test",
            source: sourceNode,
            destination: columnNode,
            metadata: { grai: { constraint_type: "TableToColumn" } },
          },
        ],
      },
    },
  },
}

test("renders", async () => {
  window.ResizeObserver = jest.fn().mockImplementation(() => ({
    disconnect: jest.fn(),
    observe: jest.fn(),
    unobserve: jest.fn(),
  }))

  renderWithMocks(<Graph />, [mock])

  await waitFor(() => {
    screen.getAllByText("N2 Node")
  })
})

// test("expand", async () => {
//   const user = userEvent.setup()

//   window.ResizeObserver = jest.fn().mockImplementation(() => ({
//     disconnect: jest.fn(),
//     observe: jest.fn(),
//     unobserve: jest.fn(),
//   }))

//   renderWithMocks(<Graph />, [mock])

//   await waitFor(() => {
//     screen.getAllByText("N2 Node")
//   })

//   await user.click(screen.getByTestId("ArrowDropDownIcon"))
// })

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
      query: GET_TABLES_AND_EDGES,
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
      query: GET_TABLES_AND_EDGES,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          tables: null,
          other_edges: null,
        },
      },
    },
  }

  renderWithMocks(<Graph />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("No nodes found")).toBeTruthy()
  })
})
