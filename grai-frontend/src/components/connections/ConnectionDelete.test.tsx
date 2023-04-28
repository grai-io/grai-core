import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import ConnectionDelete, { DELETE_CONNECTION } from "./ConnectionDelete"

const connection = {
  id: "1",
  name: "Test Connection",
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<ConnectionDelete connection={connection} onClose={() => {}} />)

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

  render(<ConnectionDelete connection={connection} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )
})

test("delete", async () => {
  const user = userEvent.setup()

  render(<ConnectionDelete connection={connection} onClose={() => {}} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )
})

test("error", async () => {
  const user = userEvent.setup()

  render(<ConnectionDelete connection={connection} onClose={() => {}} />, {
    mocks: [
      {
        request: {
          query: DELETE_CONNECTION,
          variables: {
            id: connection.id,
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
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )

  await waitFor(() => {
    expect(
      screen.getByText("Failed to delete connection ApolloError: Error!")
    ).toBeInTheDocument()
  })
})
