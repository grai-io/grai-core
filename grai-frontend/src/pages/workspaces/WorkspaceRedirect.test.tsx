import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import WorkspaceRedirect, { GET_WORKSPACE } from "./WorkspaceRedirect"

test("renders", async () => {
  renderWithRouter(<WorkspaceRedirect />, {
    route: "/workspaces/1234",
    path: "/workspaces/:workspaceId",
    routes: ["/:organisationName/:workspaceName"],
  })

  expect(screen.getByRole("progressbar")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_WORKSPACE,
      variables: {
        workspaceId: "1234",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<WorkspaceRedirect />, [mock], {
    route: "/workspaces/1234",
    path: "/workspaces/:workspaceId",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})
