import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Commits, { GET_COMMITS } from "./Commits"

test("renders", async () => {
  render(<Commits />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText(/Hello world/i)).toBeTruthy()
  })
})

test("renders branch", async () => {
  render(<Commits />, {
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
    route: "/org/demo/reports/github/owner/repo?branch=aBranch",
  })

  await waitFor(() => {
    expect(screen.getAllByText(/Hello world/i)).toBeTruthy()
  })
})

test("row click", async () => {
  const user = userEvent.setup()

  const { container } = render(<Commits />, {
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
    route: "/org/demo/reports/github/owner/repo",
    routes: [
      "/:organisationName/:workspaceName/reports/:type/:owner/:repo/commits/:reference",
    ],
  })

  await waitFor(() => {
    expect(screen.getAllByText(/Hello world/i)).toBeTruthy()
  })

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
        query: GET_COMMITS,
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

  render(<Commits />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
    route: "/org/demo/reports/github/owner/repo",
  })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_COMMITS,
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

  render(<Commits />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
    route: "/org/demo/reports/github/owner/repo",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
