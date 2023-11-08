import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import SearchControl from "./SearchControl"

test("renders", async () => {
  let value = null
  const setValue = (input: string | null) => (value = input)

  render(<SearchControl value={value} onChange={setValue} />)

  expect(screen.getByTestId("SearchIcon")).toBeInTheDocument()
  // expect(screen.getByText("Search")).toBeInTheDocument()
})

test("change", async () => {
  let value = null
  const setValue = (input: string | null) => (value = input)

  const user = userEvent.setup()

  render(<SearchControl value={value} onChange={setValue} />)

  expect(value).toEqual(null)

  await act(
    async () => await user.type(screen.getByRole("textbox"), "SearchString"),
  )

  expect(value).toEqual("g")
})

test("clear", async () => {
  let value: string | null = "search"
  const setValue = (input: string | null) => (value = input)

  const user = userEvent.setup()

  render(<SearchControl value={value} onChange={setValue} />)

  expect(value).toEqual("search")

  expect(screen.getByTestId("CloseIcon")).toBeInTheDocument()

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  expect(value).toEqual(null)
})
