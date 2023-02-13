import React from "react"
import { render, screen } from "testing"
import NotFound from "./NotFound"

test("renders", async () => {
  render(<NotFound />)

  expect(screen.getByText("Page not found")).toBeInTheDocument()
})
