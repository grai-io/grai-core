import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import ApiKeys, { GET_API_KEYS } from "./ApiKeys"

test("renders", async () => {
  render(<ApiKeys />, {
    withRouter: true,
  })

  await waitFor(() => {
    screen.getByText("Settings")
  })

  await waitFor(() => {
    screen.getByRole("heading", { name: /Api Keys/i })
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_API_KEYS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ApiKeys />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_API_KEYS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<ApiKeys />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})
