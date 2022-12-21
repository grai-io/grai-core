import React from "react"
import { render, screen, waitFor } from "testing"
import Loading from "./Loading"

test("renders", async () => {
  render(<Loading />)

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeTruthy()
  })
})

test("message", async () => {
  render(<Loading message="message" />)

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("message")).toBeTruthy()
  })
})
