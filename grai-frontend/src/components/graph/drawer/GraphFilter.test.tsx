import userEvent from "@testing-library/user-event"
import { act } from "react-dom/test-utils"
import { fireEvent, render, screen, waitFor } from "testing"
import GraphFilter from "./GraphFilter"
import useFilters from "../useFilters"

const filter = {
  id: "1",
  name: "test",
  display_name: "test",
}

test("renders", async () => {
  render(<GraphFilter filter={filter} filters={[]} setFilters={() => {}} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("test")).toBeInTheDocument()
  })
})

test("click", async () => {
  const user = userEvent.setup()

  const GraphWrapper: React.FC = () => {
    const { filters, setFilters } = useFilters()

    return (
      <GraphFilter
        filter={filter}
        filters={filters ?? []}
        setFilters={setFilters}
      />
    )
  }

  render(<GraphWrapper />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("test")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByText("test"))
  })

  await act(async () => {
    await user.click(screen.getByText("test"))
  })
})

test("hover", async () => {
  render(<GraphFilter filter={filter} filters={[]} setFilters={() => {}} />, {
    path: ":organisationName/:workspaceName/graph",
    route: "/default/demo/graph",
  })

  await waitFor(() => {
    expect(screen.getByText("test")).toBeInTheDocument()
  })

  fireEvent.mouseEnter(screen.getByText("test"))

  await waitFor(() => {
    expect(screen.getByTestId("EditIcon")).toBeInTheDocument()
  })

  fireEvent.mouseLeave(screen.getByText("test"))
})
