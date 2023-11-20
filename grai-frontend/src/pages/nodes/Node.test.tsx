import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { filtersMock } from "pages/Graph.test"
import { GET_TABLES_AND_EDGES } from "components/tables/TableLineage"
import Node, { GET_NODE } from "./Node"

export const tableMock = {
  request: {
    query: GET_NODE,
    variables: {
      organisationName: "default",
      workspaceName: "demo",
      nodeId: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        node: {
          id: "1",
          namespace: "default",
          name: "Table1",
          display_name: "Table1",
          is_active: true,
          metadata: {
            grai: {
              tags: ["tag1", "tag2"],
            },
          },
          columns: {
            data: [
              {
                id: "1",
                name: "Column1",
                display_name: "Column1",
                requirements_edges: { data: [] },
                metadata: {},
              },
            ],
          },
          source_tables: {
            data: [
              {
                id: "2",
                name: "Table2",
                display_name: "Table2",
              },
            ],
          },
          destination_tables: {
            data: [
              {
                id: "3",
                name: "Table3",
                display_name: "Table3",
              },
            ],
          },
          events: {
            data: [],
          },
          data_sources: {
            data: [],
          },
        },
      },
    },
  },
}

const mocks = [tableMock]

test("renders", async () => {
  render(<Node />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_NODE,
        variables: {
          organisationName: "",
          workspaceName: "",
          nodeId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Node />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_NODE,
        variables: {
          organisationName: "",
          workspaceName: "",
          nodeId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            node: null,
            graph: [],
          },
        },
      },
    },
  ]

  render(<Node />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("lineage", async () => {
  const user = userEvent.setup()

  const mocks = [
    filtersMock,
    filtersMock,
    tableMock,
    tableMock,
    tableMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
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
            ],
          },
        },
      },
    },
  ]

  render(<Node />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("Lineage")).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /Lineage/i })),
  )

  await waitFor(() => {
    expect(screen.getByTestId("table-lineage")).toBeInTheDocument()
  })
})

test("expand all", async () => {
  const user = userEvent.setup()

  render(<Node />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /Expand all rows/i }),
      ),
  )

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /Collapse all rows/i }),
      ),
  )
})

test("click row", async () => {
  const user = userEvent.setup()

  render(<Node />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Table1")).toBeTruthy()
  })

  await act(
    async () =>
      await user.click(
        // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
        screen.getByTestId("columns-table").querySelectorAll("tbody > tr")[0],
      ),
  )

  await act(
    async () =>
      await user.click(
        // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
        screen.getByTestId("columns-table").querySelectorAll("tbody > tr")[0],
      ),
  )
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Node />, {
    mocks,
    withRouter: true,
    path: ":organisationName/:workspaceName",
    route: "/default/demo/",
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(
    async () =>
      await user.type(screen.getByTestId("node-search"), "Search Columns"),
  )
})
