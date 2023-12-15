import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import { DELETE_CONNECTION } from "components/connections/ConnectionDelete"
import { RUN_CONNECTION } from "components/connections/ConnectionRun"
import Connection, { GET_CONNECTION } from "./Connection"

test("renders", async () => {
  render(<Connection />, {
    withRouter: true,
  })

  await screen.findAllByText("Connection 1")
})

test("refresh", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "",
          workspaceName: "",
          connectionId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            connection: {
              id: "1",
              name: "Connection 1",
              namespace: "default",
              validated: true,
              connector: {
                id: "1",
                name: "c1",
                metadata: {},
                icon: null,
                events: true,
              },
              metadata: {},
              schedules: null,
              is_active: true,
              created_at: "1234",
              updated_at: "1234",
              last_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              last_successful_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              runs: {
                data: [
                  {
                    id: "1",
                    status: "success",
                    created_at: "12243",
                    started_at: null,
                    finished_at: null,
                    metadata: {},
                    user: {
                      id: "1",
                      first_name: null,
                      last_name: null,
                    },
                  },
                  {
                    id: "2",
                    status: "success",
                    created_at: "12243",
                    started_at: null,
                    finished_at: null,
                    metadata: {},
                    user: null,
                  },
                ],
                meta: {
                  total: 2,
                },
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: RUN_CONNECTION,
        variables: {
          connectionId: "1",
          action: "UPDATE",
        },
      },
      result: {
        data: {
          runConnection: {
            id: "1",
            connection: {
              id: "1",
              last_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              last_successful_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              runs: { data: [] },
            },
          },
        },
      },
    },
  ]

  render(<Connection />, { mocks, withRouter: true })

  await screen.findAllByText("Connection 1")

  await act(async () => await user.click(screen.getByTestId("PlayArrowIcon")))

  await screen.findAllByText("Success")
})

test("refresh no last_sucessful_run", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "",
          workspaceName: "",
          connectionId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            connection: {
              id: "1",
              name: "Connection 1",
              namespace: "default",
              validated: true,
              connector: {
                id: "1",
                name: "c1",
                metadata: {},
                icon: null,
                events: false,
              },
              metadata: {},
              schedules: null,
              is_active: true,
              created_at: "1234",
              updated_at: "1234",
              last_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              last_successful_run: null,
              runs: {
                data: [
                  {
                    id: "1",
                    status: "success",
                    created_at: "12243",
                    started_at: null,
                    finished_at: null,
                    metadata: {},
                    user: {
                      id: "1",
                      first_name: null,
                      last_name: null,
                    },
                  },
                  {
                    id: "2",
                    status: "success",
                    created_at: "12243",
                    started_at: null,
                    finished_at: null,
                    metadata: {},
                    user: null,
                  },
                ],
                meta: {
                  total: 2,
                },
              },
            },
          },
        },
      },
    },
    {
      request: {
        query: RUN_CONNECTION,
        variables: {
          connectionId: "1",
          action: "UPDATE",
        },
      },
      result: {
        data: {
          runConnection: {
            id: "1",
            connection: {
              id: "1",
              last_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              last_successful_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              runs: { data: [], meta: { total: 0 } },
            },
          },
        },
      },
    },
  ]

  render(<Connection />, { mocks, withRouter: true })

  await screen.findAllByText("Connection 1")

  await act(async () => await user.click(screen.getByTestId("PlayArrowIcon")))

  await screen.findAllByText("Success")
})

test("delete", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "",
          workspaceName: "",
          connectionId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            connection: {
              id: "1",
              namespace: "default",
              name: "Connection 1",
              validated: true,
              connector: {
                id: "1",
                name: "c1",
                metadata: null,
                icon: null,
                events: true,
              },
              metadata: null,
              schedules: null,
              is_active: true,
              created_at: "1234",
              updated_at: "1234",
              last_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              last_successful_run: {
                id: "1",
                status: "success",
                created_at: "12243",
                started_at: null,
                finished_at: null,
                metadata: {},
                user: {
                  id: "1",
                  first_name: null,
                  last_name: null,
                },
              },
              runs: { data: [], meta: { total: 0 } },
            },
          },
        },
      },
    },
    {
      request: {
        query: DELETE_CONNECTION,
        variables: {
          id: "1",
        },
      },
      result: {
        data: {
          deleteConnection: {
            id: "1",
          },
        },
      },
    },
  ]

  render(<Connection />, {
    routes: ["/:organisationName/:workspaceName/connections"],
    mocks,
  })

  await screen.findByRole("heading", { name: /Connection 1/i })

  await act(async () => {
    await user.click(screen.getByTestId("MoreHorizIcon"))
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )

  await screen.findByText("New Page")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "",
          workspaceName: "",
          connectionId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Connection />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "",
          workspaceName: "",
          connectionId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            connection: null,
          },
        },
      },
    },
  ]

  render(<Connection />, { mocks, withRouter: true })

  await screen.findAllByText("Page not found")
})
