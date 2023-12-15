import { render, screen } from "testing"
import GettingStarted from "./GettingStarted"

test("renders", async () => {
  render(<GettingStarted />, {
    withRouter: true,
  })

  await screen.findByText("Getting Started")
})
