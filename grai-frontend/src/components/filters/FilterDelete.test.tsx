import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import FilterDelete, { DELETE_FILTER } from "./FilterDelete"

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

test("error", async () => {
  const user = userEvent.setup()

  render(<FilterDelete filter={filter} onClose={() => {}} />, {
    mocks: [
      {
        request: {
          query: DELETE_FILTER,
          variables: {
            id: filter.id,
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
      screen.getByText("Failed to delete filter ApolloError: Error!")
    ).toBeInTheDocument()
  })
})
