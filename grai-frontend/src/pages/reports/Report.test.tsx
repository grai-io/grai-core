import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import { destinationTable, sourceTable, spareTable } from "helpers/testNodes"
import Report, { GET_RUN } from "./Report"

test("renders", async () => {
  render(<Report />, {
    withRouter: true,
  })

  await screen.findByText("Failures")

  await screen.findByText("Failed")
})

test("renders failed", async () => {
  const user = userEvent.setup()

  render(<Report />, {
    withRouter: true,
  })

  await screen.findByText("Failures")

  await screen.findByText("Failed")

  await act(async () => {
    await user.click(screen.getByText("Failed"))
  })

  await screen.findByText("Changed Node")
})

test("not found", async () => {
  const mocks = [
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
            graph: [sourceTable, destinationTable, spareTable],
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

  await screen.findByText("Page not found")
})

test("error", async () => {
  const mocks = [
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

  await screen.findByText("Error!")
})
