import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import PullRequests, { GET_PULL_REQUESTS } from "./PullRequests"

test("renders", async () => {
  render(<PullRequests />, {
    withRouter: true,
  })

  await screen.findAllByText(/Hello world/i)
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<PullRequests />, {
    routes: ["/undefined/undefined/reports//:owner/:repo/pulls/:reference"],
  })

  await screen.findAllByText(/Hello world/i)

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0]),
  )

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

  await screen.findByText("Page not found")
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

  await screen.findByText("Error!")
})
