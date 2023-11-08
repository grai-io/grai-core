import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor, within } from "testing"
import Edges, { GET_EDGES } from "./Edges"

test("renders", async () => {
  render(<Edges />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Edges/i })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_EDGES,
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

  render(<Edges />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_EDGES,
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
            edges: {
              data: [
                {
                  id: "1",
                  namespace: "default",
                  name: "Edge 1",
                  display_name: "Edge 1",
                  is_active: true,
                  data_sources: { data: [] },
                  metadata: {},
                  source: {
                    id: "1",
                    namespace: "default",
                    name: "source 1",
                    display_name: "source 1",
                  },
                  destination: {
                    id: "2",
                    namespace: "default",
                    name: "source 1",
                    display_name: "source 1",
                  },
                },
              ],
              meta: {
                filtered: 0,
                total: 0,
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_EDGES,
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
            edges: {
              data: [],
              meta: {
                filtered: 0,
                total: 0,
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_EDGES,
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
            edges: {
              data: [],
              meta: {
                filtered: 0,
                total: 0,
              },
            },
          },
        },
      },
    },
  ]

  render(<Edges />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Edge 1")).toBeTruthy()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Se"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Se")
  })

  await waitFor(() => {
    expect(screen.getByText("No edges found")).toBeInTheDocument()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Edges />, {
    withRouter: true,
  })

  await act(async () => await user.click(screen.getByTestId("table-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Edges />, {
    routes: ["/:edgeId"],
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

test("no edges", async () => {
  const mocks = [
    {
      request: {
        query: GET_EDGES,
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
            edges: {
              data: [],
              meta: {
                filtered: 0,
                total: 0,
              },
            },
          },
        },
      },
    },
  ]

  render(<Edges />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("No edges found")).toBeInTheDocument()
  })
})

test("filter", async () => {
  render(<Edges />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Edges/i })).toBeInTheDocument()
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
})
