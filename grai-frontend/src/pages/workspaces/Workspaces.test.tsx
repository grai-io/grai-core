import React from "react"
import { render, screen, waitFor } from "testing"
import Workspaces from "./Workspaces"

test("renders", async () => {
  render(<Workspaces />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Select workspace/i })
    ).toBeInTheDocument()
  })
})
