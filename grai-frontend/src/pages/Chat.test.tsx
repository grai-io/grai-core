import { render, screen } from "testing"
import Chat from "./Chat"

jest.mock("remark-gfm", () => () => {})

test("renders", async () => {
  render(<Chat />)

  await screen.findByText("GrAI Chat")

  await screen.findByText("Is there a customer table in the prod namespace?")
})
