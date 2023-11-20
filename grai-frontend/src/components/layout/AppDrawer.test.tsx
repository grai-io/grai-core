import { userEvent } from "@testing-library/user-event"
import { act, fireEvent, render, screen, waitFor } from "testing"
import AppDrawer from "./AppDrawer"

test("renders", async () => {
  render(<AppDrawer />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Graph")).toBeTruthy()
  })
})

test("collapse", async () => {
  const user = userEvent.setup()

  render(<AppDrawer />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Graph")).toBeTruthy()
  })

  fireEvent.mouseEnter(screen.getByText("Graph"))

  await waitFor(() => {
    expect(screen.getByTestId("LeftIcon")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByTestId("LeftIcon")))

  await waitFor(() => {
    expect(screen.queryByTestId("LeftIcon")).not.toBeInTheDocument()
  })
})
