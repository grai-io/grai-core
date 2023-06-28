import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { ReactFlowProvider } from "reactflow"
import { act, render, screen, waitFor } from "testing"
import { searchMock } from "pages/Graph.test"
import GraphSearch, { SEARCH_TABLES } from "./GraphSearch"

const mocks = [
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

test("renders", async () => {
  let search: string | null = ""

  render(
    <ReactFlowProvider>
      <GraphSearch
        search={search}
        onSearch={(value: string | null) => {
          search = value
        }}
      />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    }
  )

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })
})

test("renders search", async () => {
  render(
    <ReactFlowProvider>
      <GraphSearch search="s" onSearch={() => {}} />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    }
  )

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("test table")).toBeInTheDocument()
  })
})

test("keyboard", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphSearch search="s" onSearch={() => {}} />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    }
  )

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("test table")).toBeInTheDocument()
  })

  await act(async () => {
    await user.keyboard("{arrowup}")
  })

  await act(async () => {
    await user.keyboard("{arrowdown}")
  })

  await act(async () => {
    await user.keyboard("{enter}")
  })

  await act(async () => {
    await user.keyboard("{escape}")
  })
})

test("click", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphSearch search="s" onSearch={() => {}} />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    }
  )

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("test table")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByText("test table"))
  })
})

test("clear", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphSearch search="s" onSearch={() => {}} />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    }
  )

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("test table")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByTestId("CloseIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("CloseIcon"))
  })
})

test("errors", async () => {
  const mocks = [
    {
      request: {
        query: SEARCH_TABLES,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          search: "s",
        },
      },
      result: { errors: [new GraphQLError("Error!")] },
    },
  ]

  render(
    <ReactFlowProvider>
      <GraphSearch search="s" onSearch={() => {}} />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    }
  )

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
