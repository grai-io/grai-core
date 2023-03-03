import React from "react"
import { GraphQLError } from "graphql"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Commit, { GET_COMMIT } from "./Commit"

test("renders", async () => {
  render(<Commit />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Hello world/i })).toBeTruthy()
  })
})

test("renders no pr", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_COMMIT,
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
              commit: {
                id: "1",
                reference: "abcdef",
                title: "commit message",
                created_at: "123",
                last_successful_run: null,
                branch: {
                  id: "1",
                  reference: "branchName",
                },
                pull_request: null,
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
            ],
          },
        },
      },
    },
  ]

  render(<Commit />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/commits/:reference",
    route: "/org/demo/reports/github/owner/repo/commits/123",
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /commit message/i })
    ).toBeTruthy()
  })
})

test("not found", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_COMMIT,
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
              commit: null,
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

  render(<Commit />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/commits/:reference",
    route: "/org/demo/reports/github/owner/repo/commits/123",
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
        query: GET_COMMIT,
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

  render(<Commit />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/commits/:reference",
    route: "/org/demo/reports/github/owner/repo/commits/123",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
