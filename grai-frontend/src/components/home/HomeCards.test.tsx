import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import HomeCards, { GET_COUNTS } from "./HomeCards"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_COUNTS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            runs: {
              meta: {
                filtered: 38,
              },
            },
            tables: {
              meta: {
                total: 2,
              },
            },
            connections: {
              meta: {
                total: 1,
              },
            },
          },
        },
      },
    },
  ]

  render(<HomeCards />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Tables/i })).toBeTruthy()
  })

  await screen.findAllByText("38")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_COUNTS,
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

  render(<HomeCards />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
