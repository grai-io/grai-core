import React from "react"
import userEvent from "@testing-library/user-event"
import { ReactFlowProvider } from "reactflow"
import { act, render, screen } from "testing"
import GraphControls from "./GraphControls"

test("renders", async () => {
  render(<GraphControls errors={false} search={null} onSearch={() => {}} />, {
    withRouter: true,
  })

  expect(screen.getByTestId("SearchIcon")).toBeInTheDocument()
  expect(screen.queryByText("Limit Graph")).toBeFalsy()
})

test("renders options", async () => {
  render(
    <ReactFlowProvider>
      <GraphControls
        errors={false}
        options={{ steps: { value: 1, setValue: (input: number) => {} } }}
        search={null}
        onSearch={() => {}}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    }
  )
})

test("renders errors", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphControls errors search={null} onSearch={() => {}} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Limit Graph")).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Limit Graph/i }))
  )
  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Limit Graph/i }))
  )
})
