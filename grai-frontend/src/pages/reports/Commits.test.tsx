import { GraphQLError } from "graphql"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import React from "react"
import { render, screen, waitFor } from "testing"
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
