import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import SaveButton from "./SaveButton"

const defaultProps = {
  workspaceId: "1",
  inlineFilters: [
    {
      type: "table",
      field: null,
      operator: null,
      value: null,
    },
  ],
}

test("renders", async () => {
  render(<SaveButton {...defaultProps} />)

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument()
  })
})

test("open and close", async () => {
  const user = userEvent.setup()

  render(<SaveButton {...defaultProps} />)

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(() => {
    expect(screen.getByTestId("CloseIcon")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))
})
