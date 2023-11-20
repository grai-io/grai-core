import { render, screen } from "testing"
import ChatHistory from "./ChatHistory"

jest.mock("remark-gfm", () => () => {})

const onInput = jest.fn()

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
    {
      message: "third message",
      sender: false,
    },
    {
      message: "fourth message",
      sender: false,
    },
  ]

  render(<ChatHistory messages={messages} choices={[]} onInput={onInput} />)

  expect(screen.getByText("first message")).toBeInTheDocument()
  expect(screen.getByText("second message")).toBeInTheDocument()
})

test("renders empty", async () => {
  render(<ChatHistory messages={[]} choices={[]} onInput={onInput} />)
})
