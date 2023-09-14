import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor, within } from "testing"
import Nodes, { GET_NODES } from "./Nodes"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
          order: {},
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
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
                  data_sources: {
                    data: [
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
    {
      request: {
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
          order: { name: "ASC" },
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
              data: [
                {
                  id: "1234",
                  name: "table2",
                  namespace: "default",
                  display_name: "table2",
                  is_active: true,
                  metadata: {
                    grai: {
                      node_type: "Table",
                      tags: ["tag1", "tag2"],
                    },
                  },
                  data_sources: {
                    data: [
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
    {
      request: {
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
          order: { name: "DESC" },
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
              data: [
                {
                  id: "1234",
                  name: "table3",
                  namespace: "default",
                  display_name: "table3",
                  is_active: true,
                  metadata: {
                    grai: {
                      node_type: "Table",
                      tags: ["tag1", "tag2"],
                    },
                  },
                  data_sources: {
                    data: [
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

  render(<Nodes />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Nodes/i })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("table1")).toBeTruthy()
  })

  await act(async () => await userEvent.click(screen.getByText("Name")))

  await waitFor(() => {
    expect(screen.getAllByText("table2")).toBeTruthy()
  })

  await act(async () => await userEvent.click(screen.getByText("Name")))

  await waitFor(() => {
    expect(screen.getAllByText("table3")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
          order: {},
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Nodes />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
          order: {},
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
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
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: "S",
          order: {},
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
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
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: "Se",
          order: {},
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
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

  render(<Nodes />, {
    mocks,
    withRouter: true,
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Se"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Se")
  })

  await waitFor(() => {
    expect(screen.getByText("No nodes found")).toBeInTheDocument()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Nodes />, {
    withRouter: true,
  })

  await act(async () => await user.click(screen.getByTestId("table-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Nodes />, {
    routes: ["/:nodeId"],
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

test("no nodes", async () => {
  const mocks = [
    {
      request: {
        query: GET_NODES,
        variables: {
          organisationName: "",
          workspaceName: "",
          offset: 0,
          search: undefined,
          order: {},
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            nodes: {
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

  render(<Nodes />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("No nodes found")).toBeInTheDocument()
  })
})

test("filter", async () => {
  const user = userEvent.setup()

  render(<Nodes />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Nodes/i })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  const autocomplete = screen.getByTestId("table-filter-choice")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "T" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))
})
