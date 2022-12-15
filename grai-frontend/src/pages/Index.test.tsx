import React from "react"
import { renderWithRouter, waitFor } from "testing"
import Index from "./Index"

test("renders", async () => {
  renderWithRouter(<Index />)

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
