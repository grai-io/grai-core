import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Nodes from "./Nodes"

test("renders", async () => {
  renderWithRouter(<Nodes />)

  await waitFor(() => {
    screen.getByRole("heading", { name: /Tables/i })
  })

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })
})
