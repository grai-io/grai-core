import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import { filtersMock } from "pages/Graph.test"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import PullRequest, { GET_PULL_REQUEST } from "./PullRequest"

test("renders", async () => {
  render(<PullRequest />, {
    withRouter: true,
  })

  await screen.findAllByRole("heading", { name: /Hello world/i })

  await screen.findByText("Failed")
})

test("renders errors", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUEST,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
          reference: "123",
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
              pull_request: {
                id: "1",
                reference: "123",
                title: "Pull Request Title",
                last_commit: {
                  id: "1",
                  reference: "abc",
                  created_at: "",
                  last_successful_run: {
                    id: "1",
                    created_at: "",
                    metadata: {
                      results: [
                        {
                          failing_node: {
                            id: "None",
                            name: "N1",
                            namespace: "default",
                          },
                          failing_node_name: "default/N1",
                          message:
                            "Node `default/PUBLIC.raw_customers.id` expected not to be unique",
                          node: {
                            id: "None",
                            name: "N2",
                            namespace: "default",
                          },
                          node_name: "default/N2",
                          type: "Uniqueness",
                        },
                      ],
                    },
                  },
                },
                branch: {
                  id: "1",
                  reference: "branchname",
                },
              },
            },
            graph: [sourceTable, destinationTable, spareTable],
            filters: {
              data: [],
            },
          },
        },
      },
    },
    filtersMock,
  ]

  render(<PullRequest />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/pulls/:reference",
    route: "/default/demo/reports/github/owner/repo/pulls/123",
  })

  await screen.findByRole("heading", { name: /Pull Request Title/i })

  await screen.findByTestId("test-edge")
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUEST,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
          reference: "123",
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
              pull_request: null,
            },
            graph: [sourceTable, destinationTable, spareTable],
            filters: {
              data: [],
            },
          },
        },
      },
    },
  ]

  render(<PullRequest />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/pulls/:reference",
    route: "/default/demo/reports/github/owner/repo/pulls/123",
  })

  await screen.findByText("Page not found")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUEST,
        variables: {
          organisationName: "default",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
          repo: "repo",
          reference: "123",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<PullRequest />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/pulls/:reference",
    route: "/default/demo/reports/github/owner/repo/pulls/123",
  })

  await screen.findByText("Error!")
})
