import userEvent from "@testing-library/user-event"
import { RUN_CONNECTION } from "components/connections/ConnectionRefresh"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Connection, { GET_CONNECTION } from "./Connection"

test("renders", async () => {
  renderWithRouter(<Connection />)

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "organisation",
          workspaceName: "workspace",
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
  ]

  renderWithMocks(<Connection />, mocks)

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })

  await user.click(screen.getByTestId("RefreshIcon"))

  await waitFor(() => {
    expect(screen.getAllByText("Success")).toBeTruthy()
  })
})

test("refresh no last_sucessful_run", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          organisationName: "organisation",
          workspaceName: "workspace",
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
  ]

  renderWithMocks(<Connection />, mocks)

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })

  await user.click(screen.getByTestId("RefreshIcon"))

  await waitFor(() => {
    expect(screen.getAllByText("Success")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_CONNECTION,
      variables: {
        organisationName: "organisation",
        workspaceName: "workspace",
        connectionId: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Connection />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("not found", async () => {
  const mock = {
    request: {
      query: GET_CONNECTION,
      variables: {
        organisationName: "organisation",
        workspaceName: "workspace",
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
  }

  renderWithMocks(<Connection />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
