import React from "react"
import { render, screen, waitFor } from "testing"
import ChatWindow from "./ChatWindow"
import userEvent from "@testing-library/user-event"

test("renders", async () => {
  render(<ChatWindow />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()
})

test("type", async () => {
  const user = userEvent.setup()

  render(<ChatWindow />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()

  user.type(screen.getByRole("textbox"), "Hello")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("Hello"))

  user.type(screen.getByRole("textbox"), "{enter}")

  await waitFor(() => {
    expect(screen.getByText("Hello")).toBeInTheDocument()
  })

  expect(screen.getByRole("textbox")).toHaveValue("")
})
