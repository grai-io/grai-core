import { userEvent } from "@testing-library/user-event"
import { act, fireEvent, render, screen, waitFor } from "testing"
import AppDrawer from "./AppDrawer"

test("renders", async () => {
  render(<AppDrawer />, {
    withRouter: true,
  })

  await screen.findByText("Graph")
})

test("collapse", async () => {
  const user = userEvent.setup()

  render(<AppDrawer />, {
    withRouter: true,
  })

  await screen.findByText("Graph")

  fireEvent.mouseEnter(screen.getByText("Graph"))

  await screen.findByTestId("LeftIcon")

  await act(async () => await user.click(screen.getByTestId("LeftIcon")))

  await waitFor(() =>
    expect(screen.queryByTestId("LeftIcon")).not.toBeInTheDocument(),
  )
})
