import userEvent from "@testing-library/user-event"
import { ReactFlowProvider } from "reactflow"
import { act, render, screen, waitFor } from "testing"
import GraphControls from "./GraphControls"

const combinedFilters = {
  filters: [],
  setFilters: jest.fn(),
  inlineFilters: [],
  setInlineFilters: jest.fn(),
}

const onSearch = jest.fn()

test("renders", async () => {
  render(
    <GraphControls
      errors={false}
      search={null}
      onSearch={onSearch}
      combinedFilters={combinedFilters}
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByTestId("SearchIcon")).toBeInTheDocument()
  expect(screen.queryByText("Limit Graph")).toBeFalsy()

  await waitFor(() =>
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument(),
  )
})

test("renders options", async () => {
  render(
    <ReactFlowProvider>
      <GraphControls
        errors={false}
        options={{ steps: { value: 1, setValue: (input: number) => {} } }}
        search={null}
        onSearch={onSearch}
        combinedFilters={combinedFilters}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )
})

test("renders errors", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphControls
        errors
        search={null}
        onSearch={onSearch}
        combinedFilters={combinedFilters}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText("Limit Graph")).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Limit Graph/i })),
  )
  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Limit Graph/i })),
  )
})
