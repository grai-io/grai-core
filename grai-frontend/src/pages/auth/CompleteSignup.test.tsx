import React from "react"
import { renderWithRouter, screen } from "testing"
import CompleteSignup from "./CompleteSignup"

test("renders", async () => {
  renderWithRouter(<CompleteSignup />, {
    route: "?token=abc&uid=1234",
    path: "/",
  })

  expect(
    screen.getByRole("heading", {
      name: /Welcome to Grai, let's get started/i,
    })
  ).toBeTruthy()
})

test("missing token", async () => {
  renderWithRouter(<CompleteSignup />, {
    route: "?uid=1234",
    path: "/",
  })

  expect(screen.getByText("Missing required token")).toBeTruthy()
})
