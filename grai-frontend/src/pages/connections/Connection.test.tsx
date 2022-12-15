import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Connection from "./Connection"

test("renders", async () => {
  renderWithRouter(<Connection />)

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })
})
