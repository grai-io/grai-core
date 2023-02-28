import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import ResetPasswordForm, { RESET_PASSWORD } from "./ResetPasswordForm"

test("submit", async () => {
  const user = userEvent.setup()

  render(<ResetPasswordForm />, {
    route: "?token=abc&uid=1234",
    path: "/",
  })

  await user.type(screen.getByTestId("password"), "password")

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Password reset, please login")).toBeInTheDocument()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: RESET_PASSWORD,
        variables: {
          token: "abc",
          uid: "1234",
          password: "password",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ResetPasswordForm />, {
    route: "?token=abc&uid=1234",
    path: "/",
    mocks,
  })

  await user.type(screen.getByTestId("password"), "password")

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
