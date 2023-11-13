import { render, screen } from "testing"
import ChatMessage from "./ChatMessage"

jest.mock("remark-gfm", () => () => {})

//Current ReactMarkdown mock prevents further testing

test("renders", async () => {
  const groupedChat = {
    sender: true,
    messages: ["Message 1"],
  }

  render(<ChatMessage groupedChat={groupedChat} />)

  expect(screen.getByText("Message 1")).toBeInTheDocument()
})
