import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import Repositories, { GET_REPOSITORIES } from "./Repositories"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            repositories: {
              data: [
                {
                  id: "1",
                  type: "github",
                  owner: "owner",
                  repo: "repo1",
                },
                {
                  id: "1",
                  type: "github",
                  owner: "owner",
                  repo: "repo2",
                },
              ],
            },
          },
        },
      },
    },
  ]

  render(<Repositories />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner",
    route: "/org/demo/reports/github/owner",
  })

  await screen.findByRole("heading", { name: /Select Repository/i })

  await screen.findByText("repo1")
  await screen.findByText("repo2")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Repositories />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner",
    route: "/org/demo/reports/github/owner",
  })

  await screen.findByText("Error!")
})

test("empty", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            repositories: { data: null },
          },
        },
      },
    },
  ]

  render(<Repositories />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner",
    route: "/org/demo/reports/github/owner",
  })

  await screen.findByRole("heading", { name: /Select Repository/i })
})
