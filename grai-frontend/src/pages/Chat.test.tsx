import React from "react"
import { render, screen, waitFor } from "testing"
import Chat from "./Chat"

test("renders", async () => {
  render(<Chat />)

  await waitFor(() => {
    expect(screen.getByText("GrAI Workspace Chat")).toBeInTheDocument()
  })
})
