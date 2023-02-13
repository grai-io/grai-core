import React from "react"
import { render, screen } from "testing"
import CompleteSignup from "./CompleteSignup"

test("renders", async () => {
  render(<CompleteSignup />, {
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
  render(<CompleteSignup />, {
    route: "?uid=1234",
    path: "/",
  })

  expect(screen.getByText("Missing required token")).toBeInTheDocument()
})
