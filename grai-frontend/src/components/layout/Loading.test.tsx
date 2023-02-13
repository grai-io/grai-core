import React from "react"
import { render, screen } from "testing"
import Loading from "./Loading"

test("renders", async () => {
  render(<Loading />)

  expect(screen.getByRole("progressbar")).toBeTruthy()
})

test("message", async () => {
  render(<Loading message="message" />)

  expect(screen.getByRole("progressbar")).toBeTruthy()
  expect(screen.getByText("message")).toBeInTheDocument()
})
