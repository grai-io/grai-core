import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import FilterForm from "./FilterForm"

test("renders", async () => {
  render(<FilterForm onSave={() => {}} tags={[]} />)

  await screen.findAllByText("Save")
})

test("close", async () => {
  const user = userEvent.setup()

  render(<FilterForm onSave={() => {}} onClose={() => {}} tags={[]} />)

  await screen.findAllByText("Cancel")

  await act(async () => {
    user.click(screen.getByTestId("CloseIcon"))
  })
})
