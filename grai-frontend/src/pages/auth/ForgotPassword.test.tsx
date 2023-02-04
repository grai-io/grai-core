import React from "react"
import { render, screen, waitFor } from "testing"
import ForgotPassword from "./ForgotPassword"

test("renders", async () => {
  render(<ForgotPassword />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", {
        name: /Enter your email to reset your password/i,
      })
    ).toBeTruthy()
  })
})
