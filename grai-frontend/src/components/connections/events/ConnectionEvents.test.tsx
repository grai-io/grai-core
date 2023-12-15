import { render, screen } from "testing"
import ConnectionEvents from "./ConnectionEvents"

const connection = {
  id: "1",
}

test("renders", async () => {
  render(<ConnectionEvents connection={connection} responsive={false} />, {
    withRouter: true,
  })

  await screen.findByText("Status")
})
