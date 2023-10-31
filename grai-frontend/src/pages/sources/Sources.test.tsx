import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Sources, { GET_SOURCES } from "./Sources"

const sourcesMock = {
  request: {
    query: GET_SOURCES,
    variables: {
      organisationName: "",
      workspaceName: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        sample_data: false,
        organisation: {
          id: "1",
        },
        sources: {
          data: [
            {
              id: "1",
              name: "Source 1",
              priority: 0,
              nodes: {
                meta: {
                  total: 1,
                },
              },
              edges: {
                meta: {
                  total: 1,
                },
              },
              connections: {
                data: [
                  {
                    id: "1",
                    name: "Connection 1",
                    validated: true,
                    connector: {
                      id: "1",
                      name: "Postgres",
                      icon: "postgres",
                    },
                    last_run: null,
                  },
                  {
                    id: "2",
                    name: "Connection 2",
                    validated: false,
                    connector: {
                      id: "1",
                      name: "Postgres",
                      icon: "postgres",
                    },
                    last_run: null,
                  },
                ],
              },
              runs: {
                meta: {
                  total: 0,
                },
              },
            },
          ],
          meta: {
            total: 1,
          },
        },
      },
    },
  },
}

test("renders", async () => {
  const mocks = [sourcesMock]

  render(<Sources />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Sources/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("Source 1")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_SOURCES,
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

  render(<Sources />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const mocks = [sourcesMock]

  const user = userEvent.setup()

  render(<Sources />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Source 1")).toBeTruthy()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Search"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Search")
  })

  await waitFor(() => {
    expect(screen.getByText("No sources found")).toBeInTheDocument()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  const mocks = [sourcesMock, sourcesMock]

  render(<Sources />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Sources/i })).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("table-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const mocks = [sourcesMock]

  const { container } = render(<Sources />, {
    mocks,
    routes: [":sourceId"],
  })

  await waitFor(() => {
    expect(screen.getByText("Source 1")).toBeTruthy()
  })

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0]),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
