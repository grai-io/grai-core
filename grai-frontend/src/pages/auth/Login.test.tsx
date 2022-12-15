import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Login from "./Login"

test("renders", async () => {
  renderWithRouter(<Login />)

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Sign in to your account/i })
    ).toBeTruthy()
  })
})
