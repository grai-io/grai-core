import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Run, { GET_RUN } from "./Run"

test("renders", async () => {
  renderWithRouter(<Run />)

  await waitFor(() => {
    expect(screen.getByText("Started")).toBeTruthy()
  })
})

test("renders errors", async () => {
  const mock = {
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
            connection: {
              id: "1",
              name: "Connection 1",
              connector: {
                id: "1",
                name: "connector 1",
              },
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
  }

  renderWithMocks(<Run />, [mock])

  await waitFor(() => {
    expect(screen.getByText("You got an error")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
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
  }

  renderWithMocks(<Run />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("not found", async () => {
  const mock = {
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
  }

  renderWithMocks(<Run />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
