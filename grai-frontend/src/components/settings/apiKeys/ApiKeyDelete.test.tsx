import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import ApiKeyDelete, { DELETE_API_KEY } from "./ApiKeyDelete"

const onClose = jest.fn()

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

  render(<ApiKeyDelete apiKey={apiKey} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

// test("cancel", async () => {
//   const user = userEvent.setup()

//   render(<ApiKeyDelete apiKey={apiKey} onClose={onClose} />)

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

  render(<ApiKeyDelete apiKey={apiKey} onClose={onClose} />)

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

  render(<ApiKeyDelete apiKey={apiKey} onClose={onClose} />, {
    mocks: [
      {
        request: {
          query: DELETE_API_KEY,
          variables: {
            id: apiKey.id,
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

  await screen.findByText("Failed to delete API key ApolloError: Error!")
})
