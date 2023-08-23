import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ValueField from "./ValueField"

const operator = {
  value: "equals",
  label: "Equals",
}

const defaultProps = {
  field: {
    value: "name",
    label: "Name",
    operators: [operator],
  },
  operator,
  filter: {
    type: "table",
    field: "name",
    operator: "equals",
    value: "test",
  },
  setFilter: () => {},
  onClose: () => {},
}

test("renders", async () => {
  render(<ValueField {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("test")
  })
})

test("renders object", async () => {
  const user = userEvent.setup()

  const operator = {
    value: "equals",
    label: "Equals",
    options: [
      { value: "test", label: "Test" },
      { value: "test2", label: "Test 2" },
    ],
  }

  const props = {
    field: {
      value: "name",
      label: "Name",
      operators: [operator],
    },
    operator,
    filter: {
      type: "table",
      field: "name",
      operator: "equals",
      value: "test",
    },
    setFilter: () => {},
    onClose: () => {},
  }

  render(<ValueField {...props} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("Test")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Test 2")).toBeInTheDocument()
  })

  await act(async () => {
    await user.keyboard("{escape}")
  })
})
