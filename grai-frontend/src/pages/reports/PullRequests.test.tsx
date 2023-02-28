import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
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

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<PullRequests />, {
    routes: [
      "/undefined/undefined/reports//Hello World/Hello World/pulls/Hello World",
    ],
  })

  await waitFor(() => {
    expect(screen.getAllByText(/Hello world/i)).toBeTruthy()
  })

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeInTheDocument()
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
