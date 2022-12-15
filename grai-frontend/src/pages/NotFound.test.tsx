import React from "react"
import { render, screen, waitFor } from "testing"
import NotFound from "./NotFound"

test("renders", async () => {
  render(<NotFound />)

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeTruthy()
  })
})
