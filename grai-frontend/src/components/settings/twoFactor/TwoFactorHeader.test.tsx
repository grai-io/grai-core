import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import TwoFactorHeader from "./TwoFactorHeader"

test("open", async () => {
  const user = userEvent.setup()

  render(<TwoFactorHeader />)

  await screen.findByRole("heading", { name: /2FA Keys/i })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /add 2fa key/i }))
  })

  await screen.findByRole("heading", { name: /add 2fa device/i })

  await act(async () => {
    await user.click(screen.getByTestId("CloseIcon"))
  })
})
