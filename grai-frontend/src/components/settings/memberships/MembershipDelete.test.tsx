import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import MembershipDelete, { DELETE_MEMBERSHIP } from "./MembershipDelete"

const onClose = jest.fn()

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

  render(<MembershipDelete membership={membership} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
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

  render(<MembershipDelete membership={membership} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

// test("cancel", async () => {
//   const user = userEvent.setup()

//   render(<MembershipDelete membership={membership} onClose={onClose} />)

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

  render(<MembershipDelete membership={membership} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )
})

test("error", async () => {
  const user = userEvent.setup()

  render(<MembershipDelete membership={membership} onClose={onClose} />, {
    mocks: [
      {
        request: {
          query: DELETE_MEMBERSHIP,
          variables: {
            id: membership.id,
          },
        },
        result: {
          errors: [new GraphQLError("Error!")],
        },
      },
    ],
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )

  await waitFor(() => {
    expect(
      screen.getByText("Failed to delete membership ApolloError: Error!"),
    ).toBeInTheDocument()
  })
})
