import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ChatWindow from "./ChatWindow"

const handleInput = jest.fn()

test("renders", async () => {
  render(<ChatWindow messages={[]} onInput={handleInput} workspaceId="1" />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()
})

test("type", async () => {
  const user = userEvent.setup()

  render(<ChatWindow messages={[]} onInput={handleInput} workspaceId="1" />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()

  await act(async () => user.type(screen.getByRole("textbox"), "Hello"))

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("Hello"))

  await act(async () => await user.type(screen.getByRole("textbox"), "{enter}"))

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue(""))

  expect(handleInput).toHaveBeenCalledWith("Hello")
})
