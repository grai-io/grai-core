import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import Alerts, { GET_ALERTS } from "./Alerts"

test("renders", async () => {
  render(<Alerts />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: "Settings" })

  await screen.findByRole("heading", { name: /Alerts/i })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_ALERTS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Alerts />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_ALERTS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<Alerts />, { mocks, withRouter: true })

  await screen.findByText("Sorry something has gone wrong")
})
