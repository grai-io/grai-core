import { render, screen } from "testing"
import TableEvents from "./TableEvents"

const table = {
  id: "1",
}

test("renders", async () => {
  render(<TableEvents table={table} responsive={false} />, {
    withRouter: true,
  })

  await screen.findByText("Status")
})
