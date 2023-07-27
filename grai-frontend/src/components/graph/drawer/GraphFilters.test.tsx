import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act } from "react-dom/test-utils"
import { render, screen, waitFor } from "testing"
import GraphFilters, { GET_FILTERS } from "./GraphFilters"

test("renders", async () => {
  render(<GraphFilters filters={[]} setFilters={() => {}} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  render(<GraphFilters filters={[]} setFilters={() => {}} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await act(async () => {
    await user.type(screen.getByTestId("search-input"), "test")
  })

  await waitFor(() => {
    expect(screen.getByTestId("CloseIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("CloseIcon"))
  })
})

test("errors", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
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
              data: [],
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_FILTERS,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          search: "t",
        },
      },
      result: { errors: [new GraphQLError("Error!")] },
    },
  ]

  render(<GraphFilters filters={[]} setFilters={() => {}} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByTestId("search-input")).toBeInTheDocument()
  })

  await act(async () => {
    await user.type(screen.getByTestId("search-input"), "t")
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
