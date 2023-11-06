import { render, screen } from "testing"
import ChatHistory from "./ChatHistory"

test("renders", async () => {
  const chats = [
    {
      message: "first message",
      sender: true,
    },
    {
      message: "second message",
      sender: false,
    },
  ]

  render(<ChatHistory chats={chats} />)

  expect(screen.getByText("first message")).toBeInTheDocument()
  expect(screen.getByText("second message")).toBeInTheDocument()
})

test("renders empty", async () => {
  render(<ChatHistory chats={[]} />)
})
