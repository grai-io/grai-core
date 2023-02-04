import React from "react"
import { render, screen, waitFor } from "testing"
import Settings from "./Settings"

test("renders", async () => {
  render(<Settings />, {
    withRouter: true,
  })

  await waitFor(() => {
    screen.getByText("Settings")
  })
})
