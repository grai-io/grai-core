import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import ReportsCard, { GET_REPORTS } from "./ReportsCard"

test("renders", async () => {
  render(<ReportsCard />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Latest Reports/i })
    ).toBeTruthy()
  })

  await screen.findAllByText("Hello World")
})

test("empty", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPORTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            runs: {
              data: [],
            },
          },
        },
      },
    },
  ]

  render(<ReportsCard />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await waitFor(() => {
    expect(screen.getByText(/No reports/i)).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPORTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ReportsCard />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
