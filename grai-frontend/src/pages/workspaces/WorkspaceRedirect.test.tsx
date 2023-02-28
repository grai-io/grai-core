import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import WorkspaceRedirect, { GET_WORKSPACE } from "./WorkspaceRedirect"

test("renders", async () => {
  render(<WorkspaceRedirect />, {
    route: "/workspaces/1234",
    path: "/workspaces/:workspaceId",
    routes: ["/:organisationName/:workspaceName"],
  })

  expect(screen.getByRole("progressbar")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          workspaceId: "1234",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceRedirect />, {
    route: "/workspaces/1234",
    path: "/workspaces/:workspaceId",
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
