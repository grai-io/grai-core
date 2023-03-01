import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Reports, { GET_REPORTS } from "./Reports"
import profileMock from "testing/profileMock"

test("renders", async () => {
  render(<Reports />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Reports/i })).toBeTruthy()
  })

  await waitFor(() => expect(screen.getAllByText("Hello World")).toBeTruthy())
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
