import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import ApiKeys, { GET_API_KEYS } from "./ApiKeys"

test("renders", async () => {
  render(<ApiKeys />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: "Settings" })

  await screen.findByRole("heading", { name: /Api Keys/i })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_API_KEYS,
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

  render(<ApiKeys />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_API_KEYS,
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

  render(<ApiKeys />, { mocks, withRouter: true })

  await screen.findByText("Sorry something has gone wrong")
})
