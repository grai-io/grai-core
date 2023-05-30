import React from "react"
import { render, screen, waitFor } from "testing"
import ConnectionEvents from "./ConnectionEvents"

const connection = {
  id: "1",
}

test("renders", async () => {
  render(<ConnectionEvents connection={connection} responsive={false} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Status")).toBeInTheDocument()
  })
})
