import { act, render, screen, waitFor } from "testing"
import TwoFactorHeader from "./TwoFactorHeader"
import userEvent from "@testing-library/user-event"

test("open", async () => {
  const user = userEvent.setup()

  render(<TwoFactorHeader />)

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /2FA Keys/i }),
    ).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /add 2fa key/i }))
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /add 2fa device/i }),
    ).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("CloseIcon"))
  })
})
