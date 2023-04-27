import { fireEvent, within } from "testing"

export const input = (autocomplete: HTMLElement, value: string = "T") => {
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })
}
