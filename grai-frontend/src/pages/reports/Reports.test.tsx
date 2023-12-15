import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import Reports, { GET_REPORTS } from "./Reports"

test("renders", async () => {
  render(<Reports />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Reports/i })

  await screen.findAllByText("Hello World")
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Reports />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Reports/i })

  await screen.findAllByText("Hello World")

  await act(async () => {
    user.click(screen.getByTestId("RefreshIcon"))
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPORTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          owner: null,
          repo: null,
          branch: null,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Reports />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await screen.findByText("Error!")
})
