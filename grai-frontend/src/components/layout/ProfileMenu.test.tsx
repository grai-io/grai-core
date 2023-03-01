import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ProfileMenu from "./ProfileMenu"

test("renders", async () => {
  render(<ProfileMenu />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByTestId("profile-menu-open")).toBeTruthy()
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("open", async () => {
  const user = userEvent.setup()

  render(<ProfileMenu />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByTestId("profile-menu-open")).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByTestId("profile-menu-open"))
  )

  await waitFor(() => {
    expect(screen.getByText("Hello World")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })
})

test("logout", async () => {
  const user = userEvent.setup()

  render(<ProfileMenu />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByTestId("profile-menu-open")).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByTestId("profile-menu-open"))
  )

  await waitFor(() => {
    expect(screen.getByText("Logout")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("Logout")))
})
