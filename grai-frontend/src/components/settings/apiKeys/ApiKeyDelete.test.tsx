import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import ApiKeyDelete from "./ApiKeyDelete"

const apiKey = {
  id: "1",
  name: "key 1",
  prefix: "1234a",
  created: "2021-01-21",
  revoked: false,
  expiryDate: null,
  createdBy: {
    id: "1",
    username: "edward",
  },
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<ApiKeyDelete apiKey={apiKey} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )
})

// test("cancel", async () => {
//   const user = userEvent.setup()

//   render(<ApiKeyDelete apiKey={apiKey} onClose={() => {}} />)

//   await act(
//     async () =>
//       await user.click(screen.getByRole("menuitem", { name: /delete/i }))
//   )

//   await act(
//     async () =>
//       await user.click(screen.getByRole("button", { name: /cancel/i }))
//   )
// })

test("delete", async () => {
  const user = userEvent.setup()

  render(<ApiKeyDelete apiKey={apiKey} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )
})
