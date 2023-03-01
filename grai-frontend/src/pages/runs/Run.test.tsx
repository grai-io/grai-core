import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Run, { GET_RUN } from "./Run"

test("renders", async () => {
  render(<Run />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Started")).toBeInTheDocument()
  })
})

test("renders errors", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_RUN,
        variables: {
          organisationName: "",
          workspaceName: "",
          runId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: {
              id: "1",
              status: "error",
              connector: {
                id: "1",
                name: "Test Connector",
              },
              connection: {
                id: "1",
                name: "Connection 1",
                connector: {
                  id: "1",
                  name: "connector 1",
                },
                runs: [],
                last_run: null,
                last_successful_run: null,
              },
              metadata: {
                error: "You got an error",
              },
              user: {
                id: "1",
                username: "testuser",
                first_name: "test",
                last_name: "user",
              },
              created_at: "1234",
              updated_at: "1234",
              started_at: "1234",
              finished_at: "1234",
            },
          },
        },
      },
    },
  ]

  render(<Run />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("You got an error")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_RUN,
        variables: {
          organisationName: "",
          workspaceName: "",
          runId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Run />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_RUN,
        variables: {
          organisationName: "",
          workspaceName: "",
          runId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: null,
          },
        },
      },
    },
  ]

  render(<Run />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
