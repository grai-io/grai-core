import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import FilterMenu from "./FilterMenu"

const combinedFilters = {
  filters: [],
  setFilters: jest.fn(),
  inlineFilters: [],
  setInlineFilters: jest.fn(),
}

const defaultProps = {
  workspaceId: "1",
  options: [
    {
      value: "1",
      label: "Test Filter",
    },
  ],
  values: {
    namespaces: [],
    tags: [],
    sources: [],
  },
  combinedFilters,
}

test("renders", async () => {
  render(<FilterMenu {...defaultProps} />, { withRouter: true })

  expect(screen.getByText("Filters")).toBeInTheDocument()
})

test("close", async () => {
  const user = userEvent.setup()

  render(<FilterMenu {...defaultProps} />, { withRouter: true })

  expect(screen.getByText("Filters")).toBeInTheDocument()

  await act(async () => await user.click(screen.getByText("Filters")))

  expect(screen.getByText(/saved filters/i)).toBeInTheDocument()

  await act(async () => await user.keyboard("{Escape}"))

  expect(screen.queryByText(/saved filters/i)).not.toBeInTheDocument()
})
