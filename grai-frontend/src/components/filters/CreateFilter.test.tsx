import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import { input } from "testing/autocomplete"
import { GET_WORKSPACE } from "pages/filters/FilterCreate"
import CreateFilter, { CREATE_FILTER } from "./CreateFilter"

const defaultProps = {
  workspaceId: "1",
  namespaces: ["namespace1"],
  tags: ["tag1", "tag2"],
  sources: [
    {
      id: "1",
      name: "source1",
    },
  ],
}

test("renders", async () => {
  render(<CreateFilter {...defaultProps} />, {
    withRouter: true,
  })

  expect(screen.getByRole("textbox", { name: /name/i })).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    withRouter: true,
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  await act(
    async () => await user.click(screen.getByTestId("filter-row-remove")),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /add filter/i })),
  )

  //input(screen.getByTestId("autocomplete-property"))
  input(screen.getByTestId("autocomplete-field"), "Tag")
  input(screen.getByTestId("autocomplete-operator"), "Contains")
  await act(async () => await user.type(screen.getByTestId("value"), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit namespace", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  // input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "namespace", 2)
  input(screen.getByTestId("autocomplete-operator"), "equals", 1)

  await screen.findByTestId("autocomplete-value")

  input(screen.getByTestId("autocomplete-value"), "t")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit namespace in", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  // input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "namespace", 2)
  input(screen.getByTestId("autocomplete-operator"), "in", 2)

  await screen.findByTestId("autocomplete-value")

  input(screen.getByTestId("autocomplete-value"), "t")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit data sources", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  // input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "tag", 3)
  input(screen.getByTestId("autocomplete-operator"), "contains")

  await screen.findByTestId("autocomplete-value")

  input(screen.getByTestId("autocomplete-value"), "s")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit data sources not in", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  // input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "tag", 3)
  input(screen.getByTestId("autocomplete-operator"), "contains", 2)

  await screen.findByTestId("autocomplete-value")

  input(screen.getByTestId("autocomplete-value"), "s")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit tags", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  // input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "tag", 4)
  input(screen.getByTestId("autocomplete-operator"), "contains", 2)

  await screen.findByTestId("autocomplete-value")

  input(screen.getByTestId("autocomplete-value"), "t")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit tags doesnt contain", async () => {
  const user = userEvent.setup()

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  // input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "tag", 4)
  input(screen.getByTestId("autocomplete-operator"), "contains", 3)

  await screen.findByTestId("autocomplete-value")

  input(screen.getByTestId("autocomplete-value"), "t")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit error", async () => {
  const user = userEvent.setup()

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
            namespaces: { data: ["namespace1"] },
            tags: { data: ["tag1"] },
          },
        },
      },
    },
    {
      request: {
        query: CREATE_FILTER,
        variables: {
          workspaceId: "1",
          name: "test filter",
          metadata: [
            {
              type: "ancestor",
              field: "tag",
              operator: "contains",
              value: null,
            },
          ],
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CreateFilter {...defaultProps} />, {
    route: "/default/demo/filters/create",
    path: "/:organisationName/:workspaceName/filters/create",
    mocks,
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter",
      ),
  )

  input(screen.getByTestId("autocomplete-property"), "Table")
  input(screen.getByTestId("autocomplete-field"), "Tag")
  input(screen.getByTestId("autocomplete-operator"), "Contains")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await screen.findByText("Error!")
})
