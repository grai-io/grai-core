import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import Workspaces from "./Workspaces"

test("renders", async () => {
  renderWithRouter(<Workspaces />)

  await waitFor(() => {
    screen.getByRole("heading", { name: /Select workspace/i })
  })
})
