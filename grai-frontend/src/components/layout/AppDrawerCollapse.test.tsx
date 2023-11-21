import { userEvent } from "@testing-library/user-event"
import { act, render, screen } from "testing"
import AppDrawerCollapse from "./AppDrawerCollapse"

const setExpanded = jest.fn()

test("renders", async () => {
  render(
    <AppDrawerCollapse
      expanded={false}
      setExpanded={setExpanded}
      hover={false}
    />,
  )

  // expect(screen.queryByTestId("RightIcon")).not.toBeInTheDocument()
  expect(screen.queryByTestId("LeftIcon")).not.toBeInTheDocument()
})

test("expand", async () => {
  const user = userEvent.setup()

  render(<AppDrawerCollapse expanded={false} setExpanded={setExpanded} hover />)

  expect(screen.getByTestId("RightIcon")).toBeInTheDocument()
  expect(screen.queryByTestId("LeftIcon")).not.toBeInTheDocument()

  await act(async () => {
    await user.click(screen.getByTestId("RightIcon"))
  })

  expect(setExpanded).toHaveBeenCalledWith(true)
})

test("collapse", async () => {
  const user = userEvent.setup()

  render(<AppDrawerCollapse expanded setExpanded={setExpanded} hover />)

  expect(screen.queryByTestId("RightIcon")).not.toBeInTheDocument()
  expect(screen.getByTestId("LeftIcon")).toBeInTheDocument()

  await act(async () => {
    await user.click(screen.getByTestId("LeftIcon"))
  })

  expect(setExpanded).toHaveBeenCalledWith(false)
})
