import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Tables, { GET_TABLES } from "./Tables"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            tables: {
              data: [
                {
                  id: "1234",
                  name: "table1",
                  namespace: "default",
                  display_name: "table1",
                  is_active: true,
                  metadata: {
                    grai: {
                      node_type: "Table",
                      tags: ["tag1", "tag2"],
                    },
                  },
                  data_sources: [
                    {
                      id: "1",
                      name: "source1",
                      connections: {
                        data: [
                          {
                            id: "1",
                            connector: {
                              id: "1",
                              name: "connector1",
                              slug: "postgres",
                            },
                          },
                        ],
                      },
                    },
                  ],
                },
              ],
              meta: {
                total: 1,
                filtered: 1,
              },
            },
          },
        },
      },
    },
  ]

  render(<Tables />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Tables/i })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("table1")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Tables />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            tables: {
              data: [],
              meta: {
                total: 0,
                filtered: 0,
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: "S",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            tables: {
              data: [],
              meta: {
                total: 0,
                filtered: 0,
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: "Se",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            tables: {
              data: [],
              meta: {
                total: 0,
                filtered: 0,
              },
            },
          },
        },
      },
    },
  ]

  render(<Tables />, {
    mocks,
    withRouter: true,
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Se"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Se")
  })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Tables />, {
    withRouter: true,
  })

  await act(async () => await user.click(screen.getByTestId("table-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Tables />, {
    routes: ["/:tableId"],
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0]),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("no tables", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            tables: {
              data: [],
              meta: {
                total: 0,
                filtered: 0,
              },
            },
          },
        },
      },
    },
  ]

  render(<Tables />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})
