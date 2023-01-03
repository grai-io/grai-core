import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import { GraphQLError } from "graphql"
import ResetPasswordForm, { RESET_PASSWORD } from "./ResetPasswordForm"

test("submit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<ResetPasswordForm />, {
    route: "?token=abc&uid=1234",
    path: "/",
  })

  await user.type(screen.getByTestId("password"), "password")

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Password reset, please login")).toBeTruthy()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mock = {
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
  }

  renderWithMocks(<ResetPasswordForm />, [mock], {
    route: "?token=abc&uid=1234",
    path: "/",
  })

  await user.type(screen.getByTestId("password"), "password")

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
