import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import SourceDelete, { DELETE_SOURCE } from "./SourceDelete"

const onClose = jest.fn()

const source = {
  id: "1",
  name: "Test Source",
  connections: {
    data: [
      {
        id: "1",
        name: "Test Connection",
        connectionType: {
          id: "1",
          name: "Test Connection Type",
        },
        connectionParameters: {
          data: [
            {
              id: "1",
              name: "Test Connection Parameter",
              value: "Test Value",
              connectionParameterType: {
                id: "1",
                name: "Test Connection Parameter Type",
              },
            },
          ],
        },
      },
    ],
  },
  runs: {
    meta: {
      total: 1,
    },
  },
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<SourceDelete source={source} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )
})

test("delete", async () => {
  const user = userEvent.setup()

  render(<SourceDelete source={source} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )
})

test("delete empty source", async () => {
  const user = userEvent.setup()

  const source = {
    id: "1",
    name: "Test Source",
    connections: {
      data: [],
    },
    runs: {
      meta: {
        total: 0,
      },
    },
  }

  render(<SourceDelete source={source} onClose={onClose} />)

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )
})

test("delete many runs", async () => {
  const user = userEvent.setup()

  const source = {
    id: "1",
    name: "Test Source",
    connections: {
      data: [],
    },
    runs: {
      meta: {
        total: 2,
      },
    },
  }

  render(<SourceDelete source={source} onClose={onClose} />)

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

  render(<SourceDelete source={source} onClose={onClose} />, {
    mocks: [
      {
        request: {
          query: DELETE_SOURCE,
          variables: {
            id: source.id,
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
      screen.getByText("Failed to delete source ApolloError: Error!"),
    ).toBeInTheDocument()
  })
})
