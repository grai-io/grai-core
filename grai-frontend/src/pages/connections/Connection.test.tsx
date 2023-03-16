import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import { DELETE_CONNECTION } from "components/connections/ConnectionDelete"
import { RUN_CONNECTION } from "components/connections/ConnectionRun"
import Connection, { GET_CONNECTION } from "./Connection"

test("renders", async () => {
  render(<Connection />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  const mocks = [
    profileMock,
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
              connector: {
                id: "1",
                name: "c1",
                metadata: {},
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
              runs: [
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
              runs: [],
            },
          },
        },
      },
    },
  ]

  render(<Connection />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("PlayArrowIcon")))

  await waitFor(() => {
    expect(screen.getAllByText("Success")).toBeTruthy()
  })
})

test("refresh no last_sucessful_run", async () => {
  const user = userEvent.setup()

  const mocks = [
    profileMock,
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
              connector: {
                id: "1",
                name: "c1",
                metadata: {},
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
              runs: [
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
              runs: [],
            },
          },
        },
      },
    },
  ]

  render(<Connection />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("PlayArrowIcon")))

  await waitFor(() => {
    expect(screen.getAllByText("Success")).toBeTruthy()
  })
})

test("delete", async () => {
  const user = userEvent.setup()

  const mocks = [
    profileMock,
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
              connector: {
                id: "1",
                name: "c1",
                metadata: null,
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
              runs: [],
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

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connection 1/i })).toBeTruthy()
  })

  await act(async () => {
    await user.click(screen.getByTestId("MoreHorizIcon"))
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
