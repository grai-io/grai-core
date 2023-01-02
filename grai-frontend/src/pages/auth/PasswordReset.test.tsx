import React from "react"
import { renderWithRouter, screen } from "testing"
import PasswordReset from "./PasswordReset"

test("renders", async () => {
  renderWithRouter(<PasswordReset />, {
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
  renderWithRouter(<PasswordReset />, {
    route: "?uid=1234",
    path: "/",
  })

  expect(screen.getByText("Missing required token")).toBeTruthy()
})
