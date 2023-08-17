/* istanbul ignore file */
import { fireEvent, within } from "testing"

export const input = (
  autocomplete: HTMLElement,
  value = "T",
  down: number = 1,
) => {
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  fireEvent.change(input, { target: { value } })
  for (let i = 0; i < down; i++) {
    fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  }
  fireEvent.keyDown(autocomplete, { key: "Enter" })
}
