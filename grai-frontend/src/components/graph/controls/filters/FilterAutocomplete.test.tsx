import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import FilterAutocomplete from "./FilterAutocomplete"

const setFilters = jest.fn()

test("renders empty", async () => {
  render(
    <FilterAutocomplete filters={[]} setFilters={setFilters} options={[]} />,
  )

  expect(screen.getByText(/No filters found/i)).toBeInTheDocument()
})

test("select", async () => {
  const user = userEvent.setup()

  render(
    <FilterAutocomplete
      filters={[]}
      setFilters={setFilters}
      options={[
        {
          value: "filter1",
          label: "filter1",
        },
      ]}
    />,
  )

  expect(screen.getByText(/filter1/i)).toBeInTheDocument()

  await act(async () => await user.click(screen.getByText(/filter1/i)))

  expect(setFilters).toHaveBeenCalledWith(["filter1"])
})

test("escape", async () => {
  const user = userEvent.setup()
  const onClose = jest.fn()

  render(
    <FilterAutocomplete
      filters={[]}
      setFilters={setFilters}
      options={[
        {
          value: "filter1",
          label: "filter1",
        },
      ]}
      onClose={onClose}
    />,
  )

  await act(async () => await user.keyboard("{Escape}"))

  expect(onClose).toHaveBeenCalled()
})

test("escape no onClose", async () => {
  const user = userEvent.setup()

  render(
    <FilterAutocomplete
      filters={[]}
      setFilters={setFilters}
      options={[
        {
          value: "filter1",
          label: null,
        },
      ]}
    />,
  )

  await act(async () => await user.keyboard("{Escape}"))
})
