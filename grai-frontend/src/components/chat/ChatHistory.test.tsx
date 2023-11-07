import { render, screen } from "testing"
import ChatHistory from "./ChatHistory"

test("renders", async () => {
  const messages = [
    {
      message: "first message",
      sender: true,
    },
    {
      message: "second message",
      sender: false,
    },
  ]

  render(<ChatHistory messages={messages} />)

  expect(screen.getByText("first message")).toBeInTheDocument()
  expect(screen.getByText("second message")).toBeInTheDocument()
})

test("renders empty", async () => {
  render(<ChatHistory messages={[]} />)
})
