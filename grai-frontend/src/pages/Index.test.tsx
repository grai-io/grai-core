import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Index, { GET_WORKSPACES } from "./Index"

test("renders", async () => {
  render(<Index />, {
    routes: ["/:organisationName/:workspaceName"],
  })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("no workspaces", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        data: {
          workspaces: [],
        },
      },
    },
  ]

  render(<Index />, { routes: ["/workspaces"], mocks })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
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
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
