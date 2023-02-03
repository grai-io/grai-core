import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithRouter, screen } from "testing"
import { ReactFlowProvider } from "reactflow"
import GraphControls from "./GraphControls"

test("renders", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <GraphControls errors={false} />
    </ReactFlowProvider>
  )

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.queryByText("Limit Graph")).toBeFalsy()
})

test("renders options", async () => {
  renderWithRouter(
    <ReactFlowProvider>
      <GraphControls
        errors={false}
        options={{ n: { value: 1, setValue: (input: number) => {} } }}
      />
    </ReactFlowProvider>
  )
})

test("zoom controls", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <GraphControls errors={false} />
    </ReactFlowProvider>
  )

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()
  expect(screen.getByTestId("FitScreenIcon")).toBeInTheDocument()

  await user.click(screen.getByTestId("AddIcon"))
  await user.click(screen.getByTestId("RemoveIcon"))
  await user.click(screen.getByTestId("FitScreenIcon"))
})

test("renders errors", async () => {
  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <GraphControls errors />
    </ReactFlowProvider>
  )

  expect(screen.getByText("Limit Graph")).toBeInTheDocument()

  await user.click(screen.getByRole("button", { name: /Limit Graph/i }))
  await user.click(screen.getByRole("button", { name: /Limit Graph/i }))
})
