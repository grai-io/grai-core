import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import Alert, { GET_ALERT } from "./Alert"

test("renders", async () => {
  render(<Alert />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: "Settings" })

  await screen.findByRole("heading", { name: /Hello World/i })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_ALERT,
        variables: {
          organisationName: "",
          workspaceName: "",
          id: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Alert />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_ALERT,
        variables: {
          organisationName: "",
          workspaceName: "",
          id: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            alert: null,
          },
        },
      },
    },
  ]

  render(<Alert />, { mocks, withRouter: true })

  await screen.findByText("Sorry something has gone wrong")
})
