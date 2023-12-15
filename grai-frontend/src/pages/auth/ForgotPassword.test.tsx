import { render, screen } from "testing"
import ForgotPassword from "./ForgotPassword"

test("renders", async () => {
  render(<ForgotPassword />, {
    withRouter: true,
  })

  await screen.findByRole("heading", {
    name: /Enter your email to reset your password/i,
  })
})
