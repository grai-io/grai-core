import userEvent from "@testing-library/user-event"
import WS from "jest-websocket-mock"
import { act, render, screen, waitFor } from "testing"
import WebsocketChat from "./WebsocketChat"

const chat = {
  id: "1",
  messages: {
    data: [],
  },
}

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

test("type", async () => {
  const user = userEvent.setup()

  render(<WebsocketChat workspace={workspace} chat={chat} />)

  expect(screen.getByRole("textbox")).toBeInTheDocument()

  user.type(screen.getByRole("textbox"), "H")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("H"))

  user.type(screen.getByRole("textbox"), "{enter}")

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue(""))

  // expect(screen.getByText("H")).toBeInTheDocument()
})

test("receive", async () => {
  render(<WebsocketChat workspace={workspace} chat={chat} />)

  await server.connected

  await act(async () => server.send(JSON.stringify({ message: "H" })))
})
