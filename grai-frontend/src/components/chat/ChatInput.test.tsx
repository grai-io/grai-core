import { act, render, screen } from "testing"
import ChatInput from "./ChatInput"
import userEvent from "@testing-library/user-event"

const onInput = jest.fn()

test("type", async () => {
  const user = userEvent.setup()

  render(<ChatInput onInput={onInput} />)

  await act(() => user.type(screen.getByRole("textbox"), "Input Message"))

  expect(screen.getByRole("textbox")).toHaveValue("Input Message")

  await act(() => user.click(screen.getByRole("button")))

  expect(onInput).toHaveBeenCalledWith("Input Message")

  expect(screen.getByRole("textbox")).toHaveValue("")
})

test("type enter", async () => {
  const user = userEvent.setup()

  render(<ChatInput onInput={onInput} />)

  await act(() => user.type(screen.getByRole("textbox"), "Input Message"))

  expect(screen.getByRole("textbox")).toHaveValue("Input Message")
  await act(() => user.type(screen.getByRole("textbox"), "{enter}"))

  expect(onInput).toHaveBeenCalledWith("Input Message")

  expect(screen.getByRole("textbox")).toHaveValue("")
})

test("type multiline", async () => {
  const user = userEvent.setup()

  render(<ChatInput onInput={onInput} />)

  await act(() => user.type(screen.getByRole("textbox"), "Input Message"))
  await act(() => user.type(screen.getByRole("textbox"), "{shift>}{enter}"))
  await act(() => user.type(screen.getByRole("textbox"), "Row2"))

  expect(screen.getByRole("textbox")).toHaveValue("Input Message\nRow2")

  await act(() => user.click(screen.getByRole("button")))

  expect(onInput).toHaveBeenCalledWith("Input Message\nRow2")

  expect(screen.getByRole("textbox")).toHaveValue("")
})
