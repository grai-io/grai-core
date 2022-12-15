import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Home from "./Home"

test("renders", async () => {
  renderWithRouter(<Home />)

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Welcome to Grai/i })
    ).toBeTruthy()
  })
})
