import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import ProfileSettings, { GET_PROFILE } from "./ProfileSettings"

test("renders", async () => {
  render(<ProfileSettings />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile Settings")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
