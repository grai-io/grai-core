import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ProfileMenu from "./ProfileMenu"

test("renders", async () => {
  render(<ProfileMenu />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })
})

test("open", async () => {
  const user = userEvent.setup()

  render(<ProfileMenu />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByText("Profile")))

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("Profile")))
})

test("logout", async () => {
  const user = userEvent.setup()

  render(<ProfileMenu />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByText("Profile")))

  await waitFor(() => {
    expect(screen.getByText("Logout")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("Logout")))
})
