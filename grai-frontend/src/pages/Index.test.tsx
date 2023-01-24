import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Index, { GET_WORKSPACES } from "./Index"

test("renders", async () => {
  renderWithRouter(<Index />, {
    routes: ["/:organisationName/:workspaceName"],
  })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_WORKSPACES,
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Index />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})
