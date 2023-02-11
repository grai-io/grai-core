import { GraphQLError } from "graphql"
import React from "react"
import Workspaces, { GET_WORKSPACES } from "./Workspaces"
import { render, screen, waitFor } from "testing"

test("renders", async () => {
  render(<Workspaces />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Select workspace/i })
    ).toBeInTheDocument()
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

  render(<Workspaces />, { mocks, withRouter: true })

  await waitFor(() => {
    screen.getByRole("heading", { name: /Create a workspace/i })
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

  render(<Workspaces />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
