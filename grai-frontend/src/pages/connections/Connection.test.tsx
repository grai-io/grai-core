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

test("error", async () => {
  const mock = {
    request: {
      query: GET_CONNECTION,
      variables: {
        workspaceId: "",
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
        workspaceId: "",
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
