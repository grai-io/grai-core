import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import ForgotPassword from "./ForgotPassword"

test("renders", async () => {
  renderWithRouter(<ForgotPassword />)

  await waitFor(() => {
    expect(
      screen.getByRole("heading", {
        name: /Enter your email to reset your password/i,
      })
    ).toBeTruthy()
  })
})
