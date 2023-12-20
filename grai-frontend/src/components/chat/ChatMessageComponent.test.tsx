import { render, screen } from "testing"
import ChatMessageComponent from "./ChatMessageComponent"

jest.mock("remark-gfm", () => () => {})

//Current ReactMarkdown mock prevents further testing

test("renders", async () => {
  render(<ChatMessageComponent sender="user" message="Message 1" />)

  expect(screen.getByText("Message 1")).toBeInTheDocument()
})
