import { render, screen, waitFor } from "testing"
import FilterItem from "./FilterItem"

const defaultProps = {
  filter: {
    type: "table",
    field: "name",
    operator: "equals",
    value: "test",
  },
  setFilter: () => {},
  field: null,
  operator: null,
  onDelete: () => {},
}

test("renders", async () => {
  render(<FilterItem {...defaultProps} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("name")).toBeInTheDocument()
  })
})
