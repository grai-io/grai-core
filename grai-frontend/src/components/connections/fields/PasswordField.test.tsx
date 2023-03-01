import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import PasswordField from "./PasswordField"

test("renders", async () => {
  render(<PasswordField label="field1" value="" onChange={() => {}} />)
})

test("edit", async () => {
  const user = userEvent.setup()

  render(<PasswordField label="field1" value="" onChange={() => {}} edit />)

  await act(async () => await user.click(screen.getByRole("button")))
})
