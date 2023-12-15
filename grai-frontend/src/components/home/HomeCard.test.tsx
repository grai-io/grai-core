import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import HomeCard from "./HomeCard"

test("renders", async () => {
  render(<HomeCard color="#FF00FF" text="test" />, {
    withRouter: true,
  })

  await screen.findByText("test")
})

test("renders link", async () => {
  const user = userEvent.setup()

  render(<HomeCard color="#FF00FF" text="test" to="new" />, {
    withRouter: true,
    routes: ["new"],
  })

  await screen.findByText("test")

  await act(async () => await user.click(screen.getByText("test")))

  await screen.findByText("New Page")
})
