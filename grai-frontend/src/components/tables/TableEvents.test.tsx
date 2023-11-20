import { render, screen, waitFor } from "testing"
import TableEvents from "./TableEvents"

const table = {
  id: "1",
}

test("renders", async () => {
  render(<TableEvents table={table} responsive={false} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Status")).toBeInTheDocument()
  })
})
