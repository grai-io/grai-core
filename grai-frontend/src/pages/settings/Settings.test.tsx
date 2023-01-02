import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Settings from "./Settings"

test("renders", async () => {
  renderWithRouter(<Settings />)

  await waitFor(() => {
    screen.getByText("Settings")
  })
})
