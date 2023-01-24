import userEvent from "@testing-library/user-event"
import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import MembershipsHeader from "./MembershipsHeader"

test("renders", async () => {
  renderWithRouter(<MembershipsHeader workspaceId="1" />)

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })
})

test("open", async () => {
  const user = userEvent.setup()

  renderWithRouter(<MembershipsHeader workspaceId="1" />)

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })

  await user.click(screen.getByRole("button", { name: /Invite user/i }))

  await user.click(screen.getByTestId("CloseIcon"))
})
