import React from "react"
import { render, screen, waitFor } from "testing"
import ConnectionCreate from "./ConnectionCreate"

test("renders", async () => {
  render(<ConnectionCreate />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Add Source")).toBeInTheDocument()
  })

  expect(screen.getByText("Select an integration")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})
