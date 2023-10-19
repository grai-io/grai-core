import React from "react"
import { render, screen, waitFor } from "testing"
import GettingStarted from "./GettingStarted"

test("renders", async () => {
  render(<GettingStarted />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Getting Started")).toBeTruthy()
  })
})
