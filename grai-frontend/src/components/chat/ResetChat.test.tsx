import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ResetChat, { CREATE_CHAT } from "./ResetChat"
import { GraphQLError } from "graphql"

test("submit", async () => {
  const user = userEvent.setup()

  render(<ResetChat workspaceId="1" />)

  expect(
    screen.getByRole("button", { name: /restart chat/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /restart chat/i })),
  )

  await waitFor(async () =>
    expect(screen.getByText("Chat restarted")).toBeInTheDocument(),
  )
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_CHAT,
        variables: {
          workspaceId: "1",
        },
      },
      errors: [new GraphQLError("Error!")],
    },
  ]

  render(<ResetChat workspaceId="1" />, { mocks })

  expect(
    screen.getByRole("button", { name: /restart chat/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /restart chat/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Failed to restart chat")).toBeInTheDocument()
  })
})
