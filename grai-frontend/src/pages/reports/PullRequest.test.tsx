import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import PullRequest, { GET_PULL_REQUEST } from "./PullRequest"

const columnNode = {
  id: "3",
  namespace: "default",
  name: "N3",
  display_name: "N3 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Column",
    },
  },
}

const sourceTable = {
  id: "1",
  namespace: "default",
  name: "N1",
  display_name: "N1",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
  columns: [columnNode],
  source_tables: [],
  destination_tables: [],
}

const destinationTable = {
  id: "2",
  namespace: "default",
  name: "N2",
  display_name: "N2 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
  columns: [],
  source_tables: [],
  destination_tables: [],
}

const spareTable = {
  id: "3",
  namespace: "default",
  name: "N3",
  display_name: "N3 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
  columns: [],
  source_tables: [],
  destination_tables: [],
}

test("renders", async () => {
  render(<PullRequest />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Hello world/i })).toBeTruthy()
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
                metadata: { grai: { constraint_type: "dbt_model" } },
              },
              // {
              //   id: "2",
              //   is_active: true,
              //   data_source: "test",
              //   source: sourceNode,
              //   destination: columnNode,
              //   metadata: { grai: { constraint_type: "TableToColumn" } },
              // },
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
              // {
              //   id: "2",
              //   is_active: true,
              //   data_source: "test",
              //   source: sourceNode,
              //   destination: columnNode,
              //   metadata: { grai: { constraint_type: "TableToColumn" } },
              // },
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
