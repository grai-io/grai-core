import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import FilterDelete from "./FilterDelete"

const filter = {
  id: "1",
  name: "Test Filter",
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<FilterDelete filter={filter} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )
})

test("delete", async () => {
  const user = userEvent.setup()

  render(<FilterDelete filter={filter} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )
})
