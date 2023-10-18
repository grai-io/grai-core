import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import WebsocketChat from "./WebsocketChat"
import WS from "jest-websocket-mock"

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

  user.type(screen.getByRole("textbox"), "Hello")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("Hello"))

  user.type(screen.getByRole("textbox"), "{enter}")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue(""))

  expect(screen.getByText("Hello")).toBeInTheDocument()
})

test("receive", async () => {
  const getUrl = () => {
    return new Promise<string>(resolve => {
      setTimeout(() => resolve(URL), 1000)
    })
  }

  render(<WebsocketChat workspace={workspace} />)

  await server.connected

  await act(async () => server.send(JSON.stringify({ message: "Hello" })))

  await waitFor(() => expect(screen.getByText("Hello")).toBeInTheDocument())
})
