import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import ApiKeys from "./ApiKeys"

test("renders", async () => {
  renderWithRouter(<ApiKeys />)

  await waitFor(() => {
    screen.getByText("Settings")
  })

  await waitFor(() => {
    screen.getByRole("heading", { name: /Api Keys/i })
  })
})
