import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import Settings, { GET_WORKSPACE } from "./Settings"

test("renders", async () => {
  render(<Settings />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
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

  render(<Settings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
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

  render(<Settings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
