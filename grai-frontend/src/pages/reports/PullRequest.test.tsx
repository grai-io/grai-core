import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import PullRequest, { GET_PULL_REQUEST } from "./PullRequest"

test("renders", async () => {
  render(<PullRequest />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getAllByRole("heading", { name: /Hello world/i })
    ).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("Failed")).toBeTruthy()
  })
})

test("renders errors", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUEST,
        variables: {
          organisationName: "org",
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
  ]

  render(<PullRequest />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/pulls/:reference",
    route: "/org/demo/reports/github/owner/repo/pulls/123",
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Pull Request Title/i })
    ).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByTestId("test-edge")).toBeTruthy()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUEST,
        variables: {
          organisationName: "org",
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
    route: "/org/demo/reports/github/owner/repo/pulls/123",
  })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_PULL_REQUEST,
        variables: {
          organisationName: "org",
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
    route: "/org/demo/reports/github/owner/repo/pulls/123",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
