import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import CommitsList, { GET_BRANCH_COMMITS } from "./CommitsList"

const repository = {
  owner: "owner",
  repo: "repo",
}

test("renders", async () => {
  render(
    <CommitsList type="github" repository={repository} reference="branch" />,
    {
      withRouter: true,
    },
  )

  await screen.findAllByText(/Hello world/i)
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_BRANCH_COMMITS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
          reference: "branch",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            repository: {
              id: "1",
              owner: "owner",
              repo: "repo",
              branch: null,
            },
          },
        },
      },
    },
  ]

  render(
    <CommitsList type="github" repository={repository} reference="branch" />,
    {
      mocks,
      path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
      route: "/org/demo/reports/github/owner/repo?branch=branch",
    },
  )

  await screen.findByText("Page not found")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_BRANCH_COMMITS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
          reference: "branch",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <CommitsList type="github" repository={repository} reference="branch" />,
    {
      mocks,
      path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
      route: "/org/demo/reports/github/owner/repo?branch=branch",
    },
  )

  await screen.findByText("Error!")
})
