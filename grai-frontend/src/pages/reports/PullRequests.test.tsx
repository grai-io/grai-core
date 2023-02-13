import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import PullRequests, { GET_PULL_REQUESTS } from "./PullRequests"

test("renders", async () => {
  render(<PullRequests />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText(/Hello world/i)).toBeTruthy()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUESTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            repository: null,
          },
        },
      },
    },
  ]

  render(<PullRequests />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/pulls",
    route: "/org/demo/reports/github/owner/repo/pulls",
  })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUESTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<PullRequests />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/pulls",
    route: "/org/demo/reports/github/owner/repo/pulls",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
