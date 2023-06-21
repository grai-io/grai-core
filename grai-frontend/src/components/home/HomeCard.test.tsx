import React from "react"
import { act, render, screen, waitFor } from "testing"
import HomeCard from "./HomeCard"
import userEvent from "@testing-library/user-event"

test("renders", async () => {
  render(<HomeCard color="#FF00FF" text="test" />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("test")).toBeInTheDocument()
  })
})

test("renders link", async () => {
  const user = userEvent.setup()

  render(<HomeCard color="#FF00FF" text="test" to="new" />, {
    withRouter: true,
    routes: ["new"],
  })

  await waitFor(() => {
    expect(screen.getByText("test")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByText("test")))

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})
