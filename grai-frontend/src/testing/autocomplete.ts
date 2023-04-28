import { fireEvent, within } from "testing"

export const input = (autocomplete: HTMLElement, value: string = "T") => {
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  fireEvent.change(input, { target: { value } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })
}
