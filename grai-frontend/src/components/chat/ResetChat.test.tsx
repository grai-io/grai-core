import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import ResetChat, { CREATE_CHAT } from "./ResetChat"

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

  await screen.findByText("Chat restarted")
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

  await screen.findByText("Failed to restart chat")
})
