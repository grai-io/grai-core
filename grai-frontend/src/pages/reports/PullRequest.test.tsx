import React from "react"
import { GraphQLError } from "graphql"
import {
  columnNode,
  destinationTable,
  sourceTable,
  spareTable,
} from "helpers/testNodes"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import PullRequest, { GET_PULL_REQUEST } from "./PullRequest"

test("renders", async () => {
  render(<PullRequest />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Hello world/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("Failed")).toBeTruthy()
  })
})

test("renders errors", async () => {
  const mocks = [
    profileMock,
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
            tables: [sourceTable, destinationTable, spareTable],
            other_edges: [
              {
                id: "1",
                is_active: true,
                data_source: "test",
                source: sourceTable,
                destination: destinationTable,
                metadata: { grai: { edge_type: "TableToTable" } },
              },
              {
                id: "2",
                is_active: true,
                data_source: "test",
                source: columnNode,
                destination: destinationTable,
                metadata: { grai: { edge_type: "ColumnToColumn" } },
              },
            ],
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
    profileMock,
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
            tables: [sourceTable, destinationTable, spareTable],
            other_edges: [
              {
                id: "1",
                is_active: true,
                data_source: "test",
                source: sourceTable,
                destination: destinationTable,
                metadata: { grai: { constraint_type: "dbt_model" } },
              },
            ],
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
    profileMock,
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
