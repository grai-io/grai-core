import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import TwoFactor, { GET_PROFILE } from "./TwoFactor"

test("renders", async () => {
  render(<TwoFactor />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: "Settings" })

  await screen.findByRole("heading", { name: /2FA Keys/i })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_PROFILE,
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<TwoFactor />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("no profile", async () => {
  const mocks = [
    {
      request: {
        query: GET_PROFILE,
      },
      result: {
        data: {
          profile: null,
        },
      },
    },
  ]

  render(<TwoFactor />, { mocks, withRouter: true })

  await screen.findByText("Sorry something has gone wrong")
})
