import userEvent from "@testing-library/user-event"
import { ReactFlowProvider } from "reactflow"
import { act, render, screen, waitFor } from "testing"
import GraphDrawer from "./GraphDrawer"

test("renders", async () => {
  render(
    <GraphDrawer
      search=""
      onSearch={() => {}}
      filters={[]}
      setFilters={() => {}}
    />,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByTestId("KeyboardArrowLeftIcon")).toBeInTheDocument()
  })
})

test("expand", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphDrawer
        search=""
        onSearch={() => {}}
        filters={[]}
        setFilters={() => {}}
      />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByTestId("KeyboardArrowLeftIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("KeyboardArrowLeftIcon"))
  })

  await waitFor(() => {
    expect(screen.getByTestId("KeyboardArrowRightIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("KeyboardArrowRightIcon"))
  })
})

test("filter", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphDrawer
        search=""
        onSearch={() => {}}
        filters={[]}
        setFilters={() => {}}
      />
    </ReactFlowProvider>,
    {
      path: ":organisationName/:workspaceName/graph",
      route: "/default/demo/graph",
    },
  )

  await waitFor(() => {
    expect(screen.getByTestId("FilterAltIcon")).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByTestId("FilterAltIcon"))
  })
})
