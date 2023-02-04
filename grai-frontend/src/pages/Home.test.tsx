import React from "react"
import { render, screen, waitFor } from "testing"
import Home from "./Home"

test("renders", async () => {
  render(<Home />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Welcome to Grai/i })
    ).toBeTruthy()
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
