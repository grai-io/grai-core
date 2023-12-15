import { render, screen } from "testing"
import Login from "./Login"

test("renders", async () => {
  render(<Login />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Welcome Back!/i })
})
