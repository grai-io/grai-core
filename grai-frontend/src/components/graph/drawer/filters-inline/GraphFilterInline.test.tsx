import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
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
            data: [],
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

test("add", async () => {
  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByTestId("AddIcon"))

  await waitFor(() => {
    expect(screen.getByText("Choose data field to add")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByRole("option", { name: /tag/i }))

  expect(setInlineFilters).toHaveBeenCalledWith([
    { field: "namespace", operator: "equals", type: "table", value: "test" },
    { field: "tag", operator: "contains", type: "table", value: null },
  ])
})

test("remove", async () => {
  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await userEvent.hover(screen.getByText("Namespace"))

  await waitFor(() => {
    expect(screen.getByTestId("DeleteIcon")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByTestId("DeleteIcon"))

  expect(setInlineFilters).toHaveBeenCalledWith([])
})

test("edit", async () => {
  render(<GraphFilterInline {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Namespace")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByText("Namespace"))

  await waitFor(() => {
    expect(
      screen.getByText("Only show Table where Namespace"),
    ).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("In")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByText("In"))

  expect(setInlineFilters).toHaveBeenCalledWith([
    {
      field: "namespace",
      operator: "in",
      type: "table",
      value: "test",
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
