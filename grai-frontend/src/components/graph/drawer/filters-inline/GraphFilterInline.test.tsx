import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor } from "testing"
import GraphFilterInline, { GET_WORKSPACE } from "./GraphFilterInline"

const setInlineFilters = jest.fn()

const defaultProps = {
  inlineFilters: [
    {
      type: "table",
      field: "namespace",
      operator: "equals",
      value: "test",
    },
  ],
  setInlineFilters,
}

const mocks = [
  {
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
            data: ["default", "test", "prod"],
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
  },
]

test("renders", async () => {
  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("Save")).toBeInTheDocument()
  })
})

test("renders multiple", async () => {
  render(
    <GraphFilterInline
      inlineFilters={[
        {
          type: "table",
          field: "namespace",
          operator: "in",
          value: [],
        },
      ]}
      setInlineFilters={setInlineFilters}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Save")).toBeInTheDocument()
  })
})

test("renders null value", async () => {
  render(
    <GraphFilterInline
      inlineFilters={[
        {
          type: "table",
          field: "namespace",
          operator: "in",
          value: null,
        },
      ]}
      setInlineFilters={setInlineFilters}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Save")).toBeInTheDocument()
  })
})

test("renders data sources", async () => {
  render(
    <GraphFilterInline
      inlineFilters={[
        {
          type: "table",
          field: "data-source",
          operator: "in",
          value: ["1", "2"],
        },
      ]}
      setInlineFilters={setInlineFilters}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Save")).toBeInTheDocument()
  })
})

test("renders not field", async () => {
  render(
    <GraphFilterInline
      inlineFilters={[
        {
          type: "table",
          field: "test",
          operator: null,
          value: null,
        },
      ]}
      setInlineFilters={setInlineFilters}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Save")).toBeInTheDocument()
  })
})

test("from search", async () => {
  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route:
      '/default/demo/graph?inline-filter=%5B%7B"type"%3A"table"%2C"field"%3A"namespace"%2C"operator"%3A"equals"%2C"value"%3A"default"%7D%5D',
  })

  await waitFor(() => {
    expect(screen.getByText("Save")).toBeInTheDocument()
  })
})

test("add", async () => {
  const user = userEvent.setup()

  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByTestId("AddIcon")))

  await waitFor(() => {
    expect(screen.getByText("Choose data field to add")).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("option", { name: /tag/i })),
  )

  expect(setInlineFilters).toHaveBeenCalledWith([
    { field: "namespace", operator: "equals", type: "table", value: "test" },
    { field: "tag", operator: "contains", type: "table", value: null },
  ])
})

test("hover", async () => {
  const user = userEvent.setup()

  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(async () => await user.hover(screen.getByText("Namespace")))

  await waitFor(() => {
    expect(screen.getByTestId("DeleteIcon")).toBeInTheDocument()
  })

  fireEvent.mouseLeave(screen.getByText("Namespace"))

  await waitFor(() => {
    expect(screen.queryByTestId("DeleteIcon")).not.toBeInTheDocument()
  })
})

test("remove", async () => {
  const user = userEvent.setup()

  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(async () => await user.hover(screen.getByText("Namespace")))

  await waitFor(() => {
    expect(screen.getByTestId("DeleteIcon")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByTestId("DeleteIcon")))

  expect(setInlineFilters).toHaveBeenCalledWith([])
})

test("edit", async () => {
  const user = userEvent.setup()

  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("Namespace")))

  await waitFor(() => {
    expect(
      screen.getByText("Only show Table where Namespace"),
    ).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /in/i })).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /in/i })),
  )

  expect(setInlineFilters).toHaveBeenCalledWith([
    {
      field: "namespace",
      operator: "in",
      type: "table",
      value: "test",
    },
  ])

  await waitFor(() => {
    expect(screen.getByText("default")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("default")))

  expect(setInlineFilters).toHaveBeenCalledWith([
    {
      field: "namespace",
      operator: "equals",
      type: "table",
      value: "default",
    },
  ])

  await act(async () => await user.type(screen.getByRole("listbox"), "test"))

  await act(async () => await user.keyboard("{escape}"))
})

test("edit multiple", async () => {
  const user = userEvent.setup()

  render(
    <GraphFilterInline
      inlineFilters={[
        {
          type: "table",
          field: "namespace",
          operator: "in",
          value: ["test"],
        },
      ]}
      setInlineFilters={setInlineFilters}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("Namespace")))

  await waitFor(() => {
    expect(
      screen.getByText("Only show Table where Namespace"),
    ).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("default")).toBeInTheDocument()
  })

  await act(
    async () =>
      await act(async () => await user.click(screen.getByText("default"))),
  )

  expect(setInlineFilters).toHaveBeenCalledWith([
    {
      field: "namespace",
      operator: "in",
      type: "table",
      value: ["test", "default"],
    },
  ])

  await act(async () => await user.keyboard("{escape}"))
})

test("edit text", async () => {
  const user = userEvent.setup()

  render(
    <GraphFilterInline
      inlineFilters={[
        {
          type: "table",
          field: "name",
          operator: "equals",
          value: "test",
        },
      ]}
      setInlineFilters={setInlineFilters}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
      mocks,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Name")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("Name")))

  await waitFor(() => {
    expect(screen.getByText("Only show Table where Name")).toBeInTheDocument()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "name2"))

  await act(async () => await user.keyboard("{escape}"))

  expect(setInlineFilters).toHaveBeenCalledWith([
    {
      field: "name",
      operator: "equals",
      type: "table",
      value: "name2",
    },
  ])
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
