import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ConnectionsMenu from "./ConnectionsMenu"

const connection = {
  id: "1",
  name: "Test Connection",
  runs: { data: [] },
  last_run: null,
  last_successful_run: null,
  connector: {
    events: true,
  }
}

test("renders", async () => {
  render(<ConnectionsMenu connection={connection} workspaceId="1" />, {
    withRouter: true,
  })
})

test("edit", async () => {
  const user = userEvent.setup()

  render(<ConnectionsMenu connection={connection} workspaceId="1" />, {
    routes: ["/:connectionId"],
  })

  await act(async () => await user.click(screen.getByTestId("MoreHorizIcon")))

  await act(async () => await user.click(screen.getByTestId("EditIcon")))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})
