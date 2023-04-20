import React from "react"
import { render, screen, waitFor } from "testing"
import Login from "./Login"

test("renders", async () => {
  render(<Login />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Welcome Back!/i })).toBeTruthy()
  })
})
