import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import ApiKeys, { GET_API_KEYS } from "./ApiKeys"

test("renders", async () => {
  render(<ApiKeys />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Api Keys/i })
    ).toBeInTheDocument()
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
    expect(screen.getByText("Error!")).toBeInTheDocument()
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
