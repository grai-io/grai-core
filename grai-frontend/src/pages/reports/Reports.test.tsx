import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Reports, { GET_REPORTS } from "./Reports"

test("renders", async () => {
  render(<Reports />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Reports/i })).toBeTruthy()
  })

  await screen.findAllByText("Hello World")
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_REPORTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          owner: null,
          repo: null,
          branch: null,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Reports />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
