import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import TwoFactor, { GET_PROFILE } from "./TwoFactor"

test("renders", async () => {
  render(<TwoFactor />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /2FA Keys/i }),
    ).toBeInTheDocument()
  })
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
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

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong"),
    ).toBeInTheDocument()
  })
})
