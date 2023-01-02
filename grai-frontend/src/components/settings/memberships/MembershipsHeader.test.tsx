import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import MembershipsHeader from "./MembershipsHeader"

test("renders", async () => {
  renderWithRouter(<MembershipsHeader />)

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })
})

test("open", async () => {
  const user = userEvent.setup()

  renderWithRouter(<MembershipsHeader />)

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })

  await user.click(screen.getByRole("button", { name: /Invite user/i }))

  await user.click(screen.getByTestId("CloseIcon"))
})
