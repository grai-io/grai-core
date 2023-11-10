import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act } from "react-dom/test-utils"
import { render, screen, waitFor } from "testing"
import FilterControl, { GET_FILTERS } from "./FilterControl"

const combinedFilters = {
  filters: [],
  setFilters: jest.fn(),
  inlineFilters: [],
  setInlineFilters: jest.fn(),
}

test("renders no filters", async () => {
  const mocks = [
    {
      request: {
        query: GET_FILTERS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "test",
            name: "test",
            namespaces: {
              data: [],
            },
            tags: {
              data: [],
            },
            sources: {
              data: [],
            },
            filters: {
              data: [],
            },
          },
        },
      },
    },
  ]

  const user = userEvent.setup()

  render(<FilterControl combinedFilters={combinedFilters} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Filters")).toBeInTheDocument()
  })

  await act(async () => {
    user.click(screen.getByText("Filters"))
  })

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /add row/i })).toBeInTheDocument()
  })

  await act(async () => {
    user.click(screen.getByRole("button", { name: /cancel/i }))
  })

  await screen.findByText(/saved filters/i)
})

test("renders filters", async () => {
  const mocks = [
    {
      request: {
        query: GET_FILTERS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "test",
            name: "test",
            namespaces: {
              data: [],
            },
            tags: {
              data: [],
            },
            sources: {
              data: [],
            },
            filters: {
              data: [
                {
                  id: "test",
                  name: "test",
                },
              ],
            },
          },
        },
      },
    },
  ]

  const user = userEvent.setup()

  render(<FilterControl combinedFilters={combinedFilters} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Filters")).toBeInTheDocument()
  })

  await act(async () => {
    user.click(screen.getByText("Filters"))
  })

  await waitFor(() => {
    expect(screen.getByText(/saved filters/i)).toBeInTheDocument()
  })

  expect(
    screen.getByRole("button", { name: /add new filter/i }),
  ).toBeInTheDocument()

  await act(async () => {
    user.click(screen.getByRole("button", { name: /add new filter/i }))
  })

  await screen.findByRole("button", { name: /add row/i })
})

test("errors", async () => {
  const mocks = [
    {
      request: {
        query: GET_FILTERS,
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

  render(<FilterControl combinedFilters={combinedFilters} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Filters")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
