import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import AlertDelete, { DELETE_ALERT } from "./AlertDelete"

const onClose = jest.fn()

const alert = {
  id: "1",
  name: "Test Alert",
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<AlertDelete alert={alert} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

test("delete", async () => {
  const user = userEvent.setup()

  render(<AlertDelete alert={alert} onClose={onClose} />)

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

  render(<AlertDelete alert={alert} onClose={onClose} />, {
    mocks: [
      {
        request: {
          query: DELETE_ALERT,
          variables: {
            id: alert.id,
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

  await screen.findByText("Failed to delete alert ApolloError: Error!")
})
