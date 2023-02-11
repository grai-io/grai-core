import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import RegisterForm from "./RegisterForm"

test("renders", async () => {
  const user = userEvent.setup()

  render(<RegisterForm />)

  await user.type(screen.getByRole("textbox", { name: /name/i }), "Test User")
  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@roundtabledata.com"
  )
  await user.type(screen.getByTestId("password"), "password")

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await user.click(screen.getByRole("button", { name: /register/i }))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
