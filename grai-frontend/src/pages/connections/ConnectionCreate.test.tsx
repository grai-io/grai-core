import React from "react"
import { render, screen, waitFor } from "testing"
import ConnectionCreate from "./ConnectionCreate"

test("renders", async () => {
  render(<ConnectionCreate />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Create Connection")).toBeTruthy()
  })

  expect(screen.getByText("Select a connector")).toBeTruthy()
})
