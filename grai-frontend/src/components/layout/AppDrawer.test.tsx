import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import AppDrawer from "./AppDrawer"

test("renders", async () => {
  render(<AppDrawer />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })
})

test("collapse", async () => {
  render(<AppDrawer />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Collapse")).toBeTruthy()
  })

  await act(async () => await userEvent.click(screen.getByText("Collapse")))

  await waitFor(() => {
    expect(screen.queryByText("Collapse")).toBeFalsy()
  })

  await act(
    async () =>
      await userEvent.click(screen.getByTestId("KeyboardArrowRightIcon"))
  )

  await waitFor(() => {
    expect(screen.getByText("Collapse")).toBeTruthy()
  })
})
