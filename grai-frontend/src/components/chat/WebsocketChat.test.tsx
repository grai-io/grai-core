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

test("renders", async () => {
  const chat = {
    id: "1",
    messages: {
      data: [
        {
          id: "1",
          message: "H",
          role: "user",
          created_at: "2021-04-20T00:00:00.000000Z",
        },
      ],
    },
  }

  render(<WebsocketChat workspace={workspace} chat={chat} />)

  expect(
    screen.queryByRole("button", {
      name: "Is there a customer table in the prod namespace?",
    }),
  ).not.toBeInTheDocument()
})

test("click choice", async () => {
  const user = userEvent.setup()

  const chat = {
    id: "1",
    messages: {
      data: [
        {
          id: "1",
          message: "H",
          role: "system",
          created_at: "2021-04-20T00:00:00.000000Z",
        },
      ],
    },
  }

  render(<WebsocketChat workspace={workspace} chat={chat} />)

  expect(
    screen.getByRole("button", {
      name: "Is there a customer table in the prod namespace?",
    }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", {
          name: "Is there a customer table in the prod namespace?",
        }),
      ),
  )
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
