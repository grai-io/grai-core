import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Graph, { GET_TABLES_AND_EDGES } from "./Graph"

const mocks = [
  profileMock,
  {
    request: {
      query: GET_TABLES_AND_EDGES,
      variables: {
        organisationName: "default",
        workspaceName: "demo",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          tables: [sourceTable, destinationTable, spareTable],
          other_edges: [
            {
              id: "1",
              is_active: true,
              data_source: "test",
              source: sourceTable,
              destination: destinationTable,
              metadata: { grai: { constraint_type: "dbt_model" } },
            },
          ],
        },
      },
    },
  },
]

test("renders", async () => {
  class ResizeObserver {
    callback: globalThis.ResizeObserverCallback

    constructor(callback: globalThis.ResizeObserverCallback) {
      this.callback = callback
    }

    observe(target: Element) {
      this.callback([{ target } as globalThis.ResizeObserverEntry], this)
    }

    unobserve() {}

    disconnect() {}
  }

  window.ResizeObserver = ResizeObserver

  render(<Graph />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
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
//     screen.getByText("N2 Node")
//   })

//   await user.click(screen.getByTestId("ArrowDropDownIcon"))
// })

test("renders with errors", async () => {
  class ResizeObserver {
    callback: globalThis.ResizeObserverCallback

    constructor(callback: globalThis.ResizeObserverCallback) {
      this.callback = callback
    }

    observe(target: Element) {
      this.callback([{ target } as globalThis.ResizeObserverEntry], this)
    }

    unobserve() {}

    disconnect() {}
  }

  window.ResizeObserver = ResizeObserver

  render(<Graph />, {
    path: "/:organisationName/:workspaceName/graph",
    route:
      "/default/demo/graph?errors=%5B%7B%22source%22%3A%20%22a%22%2C%20%22destination%22%3A%20%22b%22%2C%20%22test%22%3A%20%22nullable%22%2C%20%22message%22%3A%20%22not%20null%22%7D%5D",
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("renders with limitGraph", async () => {
  class ResizeObserver {
    callback: globalThis.ResizeObserverCallback

    constructor(callback: globalThis.ResizeObserverCallback) {
      this.callback = callback
    }

    observe(target: Element) {
      this.callback([{ target } as globalThis.ResizeObserverEntry], this)
    }

    unobserve() {}

    disconnect() {}
  }

  window.ResizeObserver = ResizeObserver

  render(<Graph />, {
    path: ":organisationName/:workspaceName/graph",
    route:
      "/default/demo/graph?limitGraph=true&errors=%5B%7B%22source%22%3A%20%22N1%22%2C%20%22destination%22%3A%20%22N2%22%2C%20%22test%22%3A%20%22nullable%22%2C%20%22message%22%3A%20%22not%20null%22%7D%5D",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
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

  render(<Graph />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no nodes", async () => {
  const mocks = [
    profileMock,
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
            tables: null,
            other_edges: null,
          },
        },
      },
    },
  ]

  render(<Graph />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  class ResizeObserver {
    callback: globalThis.ResizeObserverCallback

    constructor(callback: globalThis.ResizeObserverCallback) {
      this.callback = callback
    }

    observe(target: Element) {
      this.callback([{ target } as globalThis.ResizeObserverEntry], this)
    }

    unobserve() {}

    disconnect() {}
  }

  window.ResizeObserver = ResizeObserver

  render(<Graph />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })

  await act(
    async () => await user.type(screen.getByTestId("search-input"), "search")
  )
})
