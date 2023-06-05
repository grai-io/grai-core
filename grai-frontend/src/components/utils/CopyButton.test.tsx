import { act, render, screen } from "testing"
import CopyButton from "./CopyButton"
import userEvent from "@testing-library/user-event"

test("renders", async () => {
  render(<CopyButton text="test" />)

  expect(screen.getByTestId("ContentCopyIcon")).toBeInTheDocument()
})

test("copy", async () => {
  const user = userEvent.setup()

  render(<CopyButton text="test" />)

  expect(screen.getByTestId("ContentCopyIcon")).toBeInTheDocument()

  await act(async () => await user.click(screen.getByTestId("ContentCopyIcon")))
})
