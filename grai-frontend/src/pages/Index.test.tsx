import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import Index, { GET_WORKSPACES } from "./Index"

test("renders", async () => {
  render(<Index />, {
    routes: ["/:organisationName/:workspaceName"],
  })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Index />, { mocks })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})
