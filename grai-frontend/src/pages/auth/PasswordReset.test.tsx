import React from "react"
import { render, screen } from "testing"
import PasswordReset from "./PasswordReset"

test("renders", async () => {
  render(<PasswordReset />, {
    route: "?token=abc&uid=1234",
    path: "/",
  })

  expect(
    screen.getByRole("heading", {
      name: /Choose a new password/i,
    })
  ).toBeTruthy()
})

test("missing token", async () => {
  render(<PasswordReset />, {
    route: "?uid=1234",
    path: "/",
  })

  expect(screen.getByText("Missing required token")).toBeInTheDocument()
})
