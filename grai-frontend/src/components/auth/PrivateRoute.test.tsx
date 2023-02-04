import React from "react"
import { render, screen, waitFor } from "testing"
import PrivateRoute from "./PrivateRoute"

test("renders", async () => {
  render(<PrivateRoute />, { withRouter: true })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("renders logged out", async () => {
  render(<PrivateRoute />, {
    loggedIn: false,
    routes: [{ path: "/login", element: <>Login</> }],
  })

  await waitFor(() => {
    expect(screen.getByText("Login")).toBeInTheDocument()
  })
})
