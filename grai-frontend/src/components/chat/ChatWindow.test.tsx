import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import ChatWindow from "./ChatWindow"

const handleInput = jest.fn()

test("renders", async () => {
  render(<ChatWindow chats={[]} onInput={handleInput} />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()
})

test("type", async () => {
  const user = userEvent.setup()

  render(<ChatWindow chats={[]} onInput={handleInput} />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()

  user.type(screen.getByRole("textbox"), "Hello")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("Hello"))

  user.type(screen.getByRole("textbox"), "{enter}")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue(""))

  expect(handleInput).toHaveBeenCalledWith("Hello")
})
