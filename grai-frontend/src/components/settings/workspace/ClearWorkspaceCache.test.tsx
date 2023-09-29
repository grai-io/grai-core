import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import ClearWorkspaceCache from "./ClearWorkspaceCache"

test("renders", async () => {
  render(<ClearWorkspaceCache />)
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<ClearWorkspaceCache />)

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /Clear Cache/i }))
  })
})
