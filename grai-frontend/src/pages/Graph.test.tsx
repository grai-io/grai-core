import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import { GET_FILTERS } from "components/graph/drawer/GraphFilters"
import { SEARCH_TABLES } from "components/graph/drawer/GraphSearch"
import Graph, { GET_TABLES_AND_EDGES } from "./Graph"
import { GET_WORKSPACE } from "components/graph/drawer/filters-inline/GraphFilterInline"

const baseFilter = {
  min_x: -500,
  max_x: 0,
  min_y: 0,
  max_y: 0,
  inline_filters: undefined,
}

export const filtersMock = {
  request: {
    query: GET_FILTERS,
    variables: {
      organisationName: "default",
      workspaceName: "demo",
      search: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        filters: {
          data: [
            {
              id: "1",
              name: "test",
              metadata: [],
            },
          ],
        },
      },
    },
  },
}

const tablesMock = {
  request: {
    query: GET_TABLES_AND_EDGES,
    variables: {
      organisationName: "default",
      workspaceName: "demo",
      filters: {
        filters: null,
        ...baseFilter,
      },
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        graph: [sourceTable, destinationTable, spareTable],
        filters: {
          data: [
            {
              id: "1",
              name: "test",
              metadata: [],
            },
          ],
        },
      },
    },
    meta: {
      total: 100,
    },
  },
}

const tablesMockWithFilter = {
  request: {
    query: GET_TABLES_AND_EDGES,
    variables: {
      organisationName: "default",
      workspaceName: "demo",
      filters: { filters: ["1"], ...baseFilter },
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        graph: [sourceTable, destinationTable, spareTable],
        filters: {
          data: [
            {
              id: "1",
              name: "test",
              metadata: [],
            },
          ],
        },
      },
    },
  },
}

export const searchMock = (search: string = "", graph_tables: any[] = []) => ({
  request: {
    query: SEARCH_TABLES,
    variables: {
      organisationName: "default",
      workspaceName: "demo",
      search,
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        graph_tables,
      },
    },
  },
})

const mocks = [
  filtersMock,
  filtersMock,
  tablesMock,
  tablesMock,
  searchMock(),
  searchMock(),
  searchMock("s", [
    {
      id: "1",
      name: "test table",
      display_name: "test table",
      data_source: "source",
      x: 0,
      y: 0,
    },
  ]),
]

jest.retryTimes(1)

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

  render(<Graph alwaysShow />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })
})

// test("renders placeholder", async () => {
//   class ResizeObserver {
//     callback: globalThis.ResizeObserverCallback

//     constructor(callback: globalThis.ResizeObserverCallback) {
//       this.callback = callback
//     }

//     observe(target: Element) {
//       this.callback([{ target } as globalThis.ResizeObserverEntry], this)
//     }

//     unobserve() {}

//     disconnect() {}
//   }

//   window.ResizeObserver = ResizeObserver

//   render(<Graph />, {
//     path: ":organisationName/:workspaceName/graph",
//     route: "/default/demo/graph",
//     mocks,
//   })

//   await waitFor(() => {
//     expect(screen.queryByText("N2 Node")).not.toBeInTheDocument()
//   })

//   await waitFor(() => {
//     expect(screen.getAllByTestId("placeholder")).toBeTruthy()
//   })
// })

test("renders empty", async () => {
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
    mocks: [
      filtersMock,
      filtersMock,
      searchMock(),
      searchMock(),
      {
        request: {
          query: GET_TABLES_AND_EDGES,
          variables: {
            organisationName: "default",
            workspaceName: "demo",
            filters: { filters: null, ...baseFilter },
          },
        },
        result: {
          data: {
            workspace: {
              id: "1",
              graph: [],
              filters: {
                data: [],
              },
            },
          },
        },
      },
    ],
  })

  // await waitFor(() => {
  //   expect(screen.getByText("Your graph is empty!")).toBeInTheDocument()
  // })
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

  render(<Graph alwaysShow />, {
    path: "/:organisationName/:workspaceName/graph",
    route:
      "/default/demo/graph?errors=%5B%7B%22source%22%3A%20%22a%22%2C%20%22destination%22%3A%20%22b%22%2C%20%22test%22%3A%20%22nullable%22%2C%20%22message%22%3A%20%22not%20null%22%7D%5D",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getAllByText("N1")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText(/1/i)).toBeTruthy()
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

  render(<Graph alwaysShow />, {
    path: ":organisationName/:workspaceName/graph",
    route:
      "/default/demo/graph?limitGraph=true&errors=%5B%7B%22source%22%3A%20%22N1%22%2C%20%22destination%22%3A%20%22N2%22%2C%20%22test%22%3A%20%22nullable%22%2C%20%22message%22%3A%20%22not%20null%22%7D%5D",
    mocks,
  })

  // const zoom = document.querySelector("#componentId")

  // if (zoom) {
  //   await act(async () => {
  //     await user.click(zoom)
  //     await user.click(zoom)
  //     await user.click(zoom)
  //     await user.click(zoom)
  //     await user.click(zoom)
  //   })
  // }

  // await waitFor(() => {
  //   expect(screen.getAllByTestId("placeholder")).toBeTruthy()
  // })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    filtersMock,
    filtersMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          filters: { filters: null, ...baseFilter },
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
    searchMock(),
    searchMock(),
  ]

  render(<Graph alwaysShow />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no nodes", async () => {
  const mocks = [
    filtersMock,
    filtersMock,
    searchMock(),
    searchMock(),
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          filters: { filters: null, ...baseFilter },
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            graph: [],
            filters: {
              data: [],
            },
          },
        },
      },
    },
  ]

  render(<Graph alwaysShow />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  // await waitFor(() => {
  //   expect(screen.getByText("Your graph is empty!")).toBeInTheDocument()
  // })
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

  render(<Graph alwaysShow />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("SearchIcon"))
  })

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await act(
    async () => await user.type(screen.getByTestId("search-input"), "s"),
  )

  await waitFor(() => {
    expect(screen.getByText("test table")).toBeInTheDocument()
  })
})

test("filter", async () => {
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

  render(<Graph alwaysShow />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph?filter=1",
    routes: ["/:organisationName/:workspaceName/filters"],
    mocks: [
      filtersMock,
      filtersMock,
      tablesMock,
      tablesMock,
      tablesMockWithFilter,
      searchMock(),
      searchMock(),
    ],
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByTestId("FilterListIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("FilterListIcon"))
  })

  await waitFor(() => {
    expect(screen.getByText("Manage Filters")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByText("Manage Filters"))
  })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("inline filter", async () => {
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

  const inlineFilterMock = (value: string = "default") => ({
    request: {
      query: GET_TABLES_AND_EDGES,
      variables: {
        organisationName: "default",
        workspaceName: "demo",
        filters: {
          filters: null,
          min_x: -500,
          max_x: 0,
          min_y: 0,
          max_y: 0,
          inline_filters: [
            {
              type: "table",
              field: "namespace",
              operator: "equals",
              value,
            },
          ],
        },
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          graph: [sourceTable, destinationTable, spareTable],
          filters: {
            data: [
              {
                id: "1",
                name: "test",
                metadata: [],
              },
            ],
          },
        },
      },
    },
  })

  const workspacesMock = {
    request: {
      query: GET_WORKSPACE,
      variables: {
        organisationName: "default",
        workspaceName: "demo",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          name: "demo",
          namespaces: {
            data: ["default", "test"],
          },
          tags: {
            data: [],
          },
          sources: {
            data: [],
          },
        },
      },
    },
  }

  render(<Graph alwaysShow />, {
    path: ":organisationName/:workspaceName/graph",
    route:
      '/default/demo/graph?inline-filter=%5B%7B"type"%3A"table"%2C"field"%3A"namespace"%2C"operator"%3A"equals"%2C"value"%3A"default"%7D%5D',
    routes: ["/:organisationName/:workspaceName/filters"],
    mocks: [
      filtersMock,
      filtersMock,
      tablesMock,
      tablesMock,
      tablesMock,
      tablesMockWithFilter,
      searchMock(),
      searchMock(),
      inlineFilterMock(),
      inlineFilterMock(),
      inlineFilterMock(),
      inlineFilterMock("test"),
      workspacesMock,
      workspacesMock,
    ],
  })

  await waitFor(() => {
    expect(screen.getByText("N2 Node")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByTestId("FilterAltIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("FilterAltIcon"))
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByText("Namespace"))
  })

  await act(async () => {
    await user.click(screen.getByText("test"))
  })

  await waitFor(async () => {
    await user.click(screen.getByTestId("DeleteIcon"))
  })
})
