import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithRouter, screen, waitFor } from "testing"
import LoginForm from "./LoginForm"

test("submit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<LoginForm />)

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )
  await user.type(screen.getByTestId("password"), "password")

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await user.click(screen.getByRole("button", { name: /login/i }))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
