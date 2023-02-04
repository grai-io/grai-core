import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import LoginForm from "./LoginForm"

test("submit", async () => {
  const user = userEvent.setup()

  render(<LoginForm />, {
    guestRoute: true,
    loggedIn: false,
    path: "/login",
    route: "/login",
    routes: ["/"],
  })

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )
  await user.type(screen.getByTestId("password"), "password")

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await user.click(screen.getByRole("button", { name: /login/i }))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  render(<LoginForm />, {
    withRouter: true,
    loggedIn: false,
    throwError: true,
  })

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )
  await user.type(screen.getByTestId("password"), "password")

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await user.click(screen.getByRole("button", { name: /login/i }))

  await waitFor(() => {
    expect(screen.getByText("Error")).toBeTruthy()
  })
})
