import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import PrivateRoute from "./PrivateRoute"

test("renders", async () => {
  renderWithRouter(<PrivateRoute />)

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("renders logged out", async () => {
  renderWithRouter(<PrivateRoute />, {
    user: null,
    routes: [{ path: "/login", element: <>Login</> }],
  })

  await waitFor(() => {
    expect(screen.getByText("Login")).toBeTruthy()
  })
})
