import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import ConnectionDelete, { DELETE_CONNECTION } from "./ConnectionDelete"

const connection = {
  id: "1",
  name: "Test Connection",
  runs: {
    meta: {
      total: 0,
    },
  },
}

const onClose = jest.fn()

test("renders", async () => {
  const user = userEvent.setup()

  render(<ConnectionDelete connection={connection} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

test("renders no name", async () => {
  const user = userEvent.setup()

  render(<ConnectionDelete connection={connection} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

test("delete", async () => {
  const user = userEvent.setup()

  render(<ConnectionDelete connection={connection} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )
})

test("delete one run", async () => {
  const user = userEvent.setup()

  const connection = {
    id: "1",
    name: "Test Connection",
    runs: {
      meta: {
        total: 1,
      },
    },
  }

  render(<ConnectionDelete connection={connection} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )
})

test("delete two runs", async () => {
  const user = userEvent.setup()

  const connection = {
    id: "1",
    name: "Test Connection",
    runs: {
      meta: {
        total: 2,
      },
    },
  }

  render(<ConnectionDelete connection={connection} onClose={onClose} />)

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

  render(<ConnectionDelete connection={connection} onClose={onClose} />, {
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
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )

  await waitFor(() => {
    expect(
      screen.getByText("Failed to delete connection ApolloError: Error!"),
    ).toBeInTheDocument()
  })
})
