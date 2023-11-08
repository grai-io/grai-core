import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import FilterForm from "./FilterForm"

const defaultProps = {
  onSave: () => {},
  namespaces: [],
  tags: [],
  sources: [],
}

test("renders", async () => {
  render(<FilterForm {...defaultProps} />)

  await screen.findByText("Save")
})

const onClose = jest.fn()

test("close", async () => {
  const user = userEvent.setup()

  render(<FilterForm {...defaultProps} onClose={onClose} />)

  expect(screen.getByText("Cancel")).toBeInTheDocument()

  await act(async () => {
    user.click(screen.getByText("Cancel"))
  })

  await waitFor(() => {
    expect(onClose).toHaveBeenCalled()
  })
})
