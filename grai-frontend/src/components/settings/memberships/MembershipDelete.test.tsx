import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import MembershipDelete from "./MembershipDelete"

const membership = {
  id: "1",
  user: {
    username: "test@example.com",
    first_name: "first",
    last_name: "last",
  },
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<MembershipDelete membership={membership} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )
})

test("renders no name", async () => {
  const membership = {
    id: "1",
    user: {
      username: "test@example.com",
      first_name: null,
      last_name: null,
    },
  }

  const user = userEvent.setup()

  render(<MembershipDelete membership={membership} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )
})

// test("cancel", async () => {
//   const user = userEvent.setup()

//   render(<MembershipDelete membership={membership} onClose={() => {}} />)

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

  render(<MembershipDelete membership={membership} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )
})
