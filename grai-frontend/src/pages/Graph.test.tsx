import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Graph from "./Graph"

test("renders", async () => {
  window.ResizeObserver =
    window.ResizeObserver ||
    jest.fn().mockImplementation(() => ({
      disconnect: jest.fn(),
      observe: jest.fn(),
      unobserve: jest.fn(),
    }))

  renderWithRouter(<Graph />)

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })
})
