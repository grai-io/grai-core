import userEvent from "@testing-library/user-event"
import React from "react"
import { render, renderWithRouter, screen, waitFor } from "testing"
import ProfileMenu from "./ProfileMenu"

test("renders", async () => {
  renderWithRouter(<ProfileMenu />)

  await waitFor(() => {
    expect(screen.getByTestId("profile-menu-open")).toBeTruthy()
  })
})

test("open", async () => {
  const user = userEvent.setup()

  renderWithRouter(<ProfileMenu />)

  await waitFor(() => {
    expect(screen.getByTestId("profile-menu-open")).toBeTruthy()
  })

  await user.click(screen.getByTestId("profile-menu-open"))

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeTruthy()
  })
})

test("logout", async () => {
  const user = userEvent.setup()

  renderWithRouter(<ProfileMenu />)

  await waitFor(() => {
    expect(screen.getByTestId("profile-menu-open")).toBeTruthy()
  })

  await user.click(screen.getByTestId("profile-menu-open"))

  await waitFor(() => {
    expect(screen.getByText("Logout")).toBeTruthy()
  })

  await user.click(screen.getByText("Logout"))
})
