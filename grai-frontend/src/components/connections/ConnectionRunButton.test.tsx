import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ConnectionRunButton from "./ConnectionRunButton"

const onRun = jest.fn()

test("renders", async () => {
  render(<ConnectionRunButton onRun={onRun} status={null} />)
})

test("run", async () => {
  const user = userEvent.setup()

  render(<ConnectionRunButton onRun={onRun} events status={null} />)

  await act(async () => await user.click(screen.getByText("Run")))

  expect(onRun).toHaveBeenCalled()
})

test("open", async () => {
  const user = userEvent.setup()

  render(<ConnectionRunButton onRun={onRun} events status={null} />)

  await act(
    async () => await user.click(screen.getByTestId("ArrowDropDownIcon")),
  )

  await waitFor(() => {
    expect(screen.getByText("Run Events")).toBeInTheDocument()
  })

  await user.click(document.body)

  await waitFor(() => {
    expect(screen.queryByText("Run Events")).not.toBeInTheDocument()
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
