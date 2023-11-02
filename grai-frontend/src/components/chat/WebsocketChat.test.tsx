import React from "react"
import userEvent from "@testing-library/user-event"
import WS from "jest-websocket-mock"
import { act, render, screen, waitFor } from "testing"
import WebsocketChat from "./WebsocketChat"

const workspace = {
  id: "1",
}

let server: WS
const URL = `ws://localhost:8000/ws/chat/${workspace.id}/`

beforeEach(() => {
  server = new WS(URL)
})

afterEach(() => {
  WS.clean()
})

test("renders", async () => {
  render(<WebsocketChat workspace={workspace} />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()
})

test("type", async () => {
  const user = userEvent.setup()

  render(<WebsocketChat workspace={workspace} />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()

  user.type(screen.getByRole("textbox"), "H")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("H"))

  user.type(screen.getByRole("textbox"), "{enter}")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue(""))

  expect(screen.getByText("H")).toBeInTheDocument()
})

test("receive", async () => {
  render(<WebsocketChat workspace={workspace} />)

  await server.connected

  await act(async () => server.send(JSON.stringify({ message: "H" })))

  await screen.findByText("H")
})
