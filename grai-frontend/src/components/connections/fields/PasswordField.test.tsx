import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import PasswordField from "./PasswordField"

const onChange = jest.fn()

test("renders", async () => {
  const user = userEvent.setup()

  render(<PasswordField label="field1" value="" onChange={onChange} />)

  await act(async () => await user.type(screen.getByLabelText(/field1/i), "t"))

  expect(onChange).toHaveBeenCalled()
})

test("edit", async () => {
  const user = userEvent.setup()

  render(<PasswordField label="field1" value="" onChange={onChange} edit />)

  await act(async () => await user.click(screen.getByRole("button")))
})
