import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Workspaces, { GET_WORKSPACES } from "./Workspaces"

test("renders", async () => {
  renderWithRouter(<Workspaces />)

  await waitFor(() => {
    screen.getByRole("heading", { name: /Select workspace/i })
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

  renderWithMocks(<Workspaces />, mocks)

  await waitFor(() => {
    screen.getByRole("heading", { name: /No workspaces/i })
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

  renderWithMocks(<Workspaces />, mocks)

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
