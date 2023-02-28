import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import ConnectionsMenu from "./ConnectionsMenu"

const connection = {
  id: "1",
  runs: [],
  last_run: null,
  last_successful_run: null,
}

test("renders", async () => {
  render(<ConnectionsMenu connection={connection} workspaceId="1" />, {
    withRouter: true,
  })
})

test("edit", async () => {
  const user = userEvent.setup()

  render(<ConnectionsMenu connection={connection} workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/connections/:connectionId"],
  })

  await user.click(screen.getByTestId("MoreHorizIcon"))

  await user.click(screen.getByTestId("EditIcon"))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})
