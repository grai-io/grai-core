import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import AddButton from "./AddButton"

const defaultProps = {
  fields: [
    {
      value: "test",
      label: "test",
      operators: [],
    },
  ],
  onAdd: () => {},
}

test("renders", async () => {
  render(<AddButton {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  })
})

test("click", async () => {
  render(<AddButton {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByTestId("AddIcon"))

  await waitFor(() => {
    expect(screen.getByText("Choose data field to add")).toBeInTheDocument()
  })
})

test("escape", async () => {
  render(<AddButton {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  })

  await userEvent.click(screen.getByTestId("AddIcon"))

  await waitFor(() => {
    expect(screen.getByText("Choose data field to add")).toBeInTheDocument()
  })

  await userEvent.keyboard("{Escape}")
})
