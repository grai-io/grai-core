import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import FilterDelete, { DELETE_FILTER } from "./FilterDelete"

const onClose = jest.fn()

const filter = {
  id: "1",
  name: "Test Filter",
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<FilterDelete filter={filter} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

test("delete", async () => {
  const user = userEvent.setup()

  render(<FilterDelete filter={filter} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )

  await screen.findByText("Filter deleted")
})

test("error", async () => {
  const user = userEvent.setup()

  render(<FilterDelete filter={filter} onClose={onClose} />, {
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
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )

  await screen.findByText("Failed to delete filter ApolloError: Error!")
})
