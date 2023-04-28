import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import FilterForm from "./FilterForm"

test("renders", async () => {
  render(<FilterForm onSave={() => {}} />)

  await screen.findAllByText("Save")
})

test("close", async () => {
  render(<FilterForm onSave={() => {}} onClose={() => {}} />)

  await screen.findAllByText("Cancel")

  await act(async () => {
    userEvent.click(screen.getByTestId("CloseIcon"))
  })
})
