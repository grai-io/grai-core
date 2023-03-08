import React from "react"
import { GraphQLError } from "graphql"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Report, { GET_RUN } from "./Report"

test("renders", async () => {
  render(<Report />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Failures")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("Failed")).toBeTruthy()
  })
})

test("not found", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_RUN,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          runId: "1234",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: null,
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

  render(<Report />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/reports/:reportId",
    route: "/org/demo/reports/github/owner/repo/reports/1234",
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
        query: GET_RUN,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          runId: "1234",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Report />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo/reports/:reportId",
    route: "/org/demo/reports/github/owner/repo/reports/1234",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
