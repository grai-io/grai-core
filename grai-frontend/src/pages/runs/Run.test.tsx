import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import Run, { GET_RUN } from "./Run"

test("renders", async () => {
  render(<Run />, {
    withRouter: true,
  })

  await screen.findByText("Started")
})

test("renders errors", async () => {
  const mocks = [
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
                events: true,
              },
              connection: {
                id: "1",
                name: "Connection 1",
                validated: true,
                connector: {
                  id: "1",
                  name: "connector 1",
                  events: false,
                },
                runs: { data: [] },
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

  await screen.findByText("You got an error")
})

test("error", async () => {
  const mocks = [
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

  await screen.findByText("Error!")
})

test("not found", async () => {
  const mocks = [
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

  await screen.findByText("Page not found")
})
