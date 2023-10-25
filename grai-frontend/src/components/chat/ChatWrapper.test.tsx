import React from "react"
import { render, screen, waitFor } from "testing"
import ChatWrapper, { FETCH_CHATS } from "./ChatWrapper"

const workspace = {
  id: "1",
}

test("renders", async () => {
  render(<ChatWrapper workspace={workspace} />)

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: FETCH_CHATS,
        variables: {
          workspaceId: "1",
        },
      },
      error: new Error("An error occurred"),
    },
  ]

  render(<ChatWrapper workspace={workspace} />, { mocks })

  await waitFor(() => {
    expect(screen.getByText("An error occurred")).toBeInTheDocument()
  })
})
