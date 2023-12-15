import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import ProfileSettings, { GET_PROFILE } from "./ProfileSettings"

test("renders", async () => {
  render(<ProfileSettings />, {
    withRouter: true,
  })

  await screen.findByText("Personal info")
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

  render(<ProfileSettings />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("not found", async () => {
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

  render(<ProfileSettings />, { mocks, withRouter: true })

  await screen.findByText("Page not found")
})
