import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Node from "./Node"

test("renders", async () => {
  renderWithRouter(<Node />)

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })
})
