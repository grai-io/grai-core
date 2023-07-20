import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import { input } from "testing/autocomplete"
import CreateFilter, { CREATE_FILTER } from "./CreateFilter"
import { GET_WORKSPACE } from "pages/filters/FilterCreate"
import { GraphQLError } from "graphql"

test("renders", async () => {
  render(<CreateFilter workspaceId="1" tags={[]} />, {
    withRouter: true,
  })

  expect(screen.getByRole("textbox", { name: /name/i })).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateFilter workspaceId="1" tags={[]} />, {
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

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /add filter/i })),
  )

  input(screen.getByTestId("autocomplete-property"), "Table")
  input(screen.getByTestId("autocomplete-field"), "Tag")
  input(screen.getByTestId("autocomplete-operator"), "Contains")
  await act(async () => await user.type(screen.getByTestId("value"), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("submit tags", async () => {
  const user = userEvent.setup()

  render(<CreateFilter workspaceId="1" tags={["tag1", "tag2"]} />, {
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

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /add filter/i })),
  )

  input(screen.getByTestId("autocomplete-property"), "table")
  input(screen.getByTestId("autocomplete-field"), "tag", 2)
  input(screen.getByTestId("autocomplete-operator"), "contains", 2)

  await waitFor(() => {
    expect(screen.getByTestId("autocomplete-value")).toBeInTheDocument()
  })

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
            { type: "table", field: "name", operator: "equals", value: null },
          ],
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CreateFilter workspaceId="1" tags={[]} />, {
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

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /add filter/i })),
  )

  input(screen.getByTestId("autocomplete-property"), "Table")
  input(screen.getByTestId("autocomplete-field"), "Tag")
  input(screen.getByTestId("autocomplete-operator"), "Contains")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
