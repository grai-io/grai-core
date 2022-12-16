import userEvent from "@testing-library/user-event"
import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import ConnectionsMenu from "./ConnectionsMenu"

const connection = {
  id: "1",
}

test("renders", async () => {
  renderWithRouter(<ConnectionsMenu connection={connection} />)
})

test("edit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<ConnectionsMenu connection={connection} />, {
    routes: ["/connections/:connectionId"],
  })

  await user.click(screen.getByTestId("MoreHorizIcon"))

  await user.click(screen.getByTestId("EditIcon"))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})
