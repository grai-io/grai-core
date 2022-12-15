import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Index from "./Index"

test("renders", async () => {
  renderWithRouter(<Index />)

  await waitFor(() => {})
})
