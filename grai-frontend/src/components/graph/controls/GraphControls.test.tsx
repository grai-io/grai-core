import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen } from "testing"
import { ReactFlowProvider } from "reactflow"
import GraphControls from "./GraphControls"

test("renders", async () => {
  render(
    <ReactFlowProvider>
      <GraphControls errors={false} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    }
  )

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.queryByText("Limit Graph")).toBeFalsy()
})

test("renders options", async () => {
  render(
    <ReactFlowProvider>
      <GraphControls
        errors={false}
        options={{ n: { value: 1, setValue: (input: number) => {} } }}
      />
    </ReactFlowProvider>,
    {
      withRouter: true,
    }
  )
})

test("zoom controls", async () => {
  const user = userEvent.setup()

  render(
    <ReactFlowProvider>
      <GraphControls errors={false} />
    </ReactFlowProvider>,
    {
      withRouter: true,
    }
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

  render(
    <ReactFlowProvider>
      <GraphControls errors />
    </ReactFlowProvider>,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Limit Graph")).toBeInTheDocument()

  await user.click(screen.getByRole("button", { name: /Limit Graph/i }))
  await user.click(screen.getByRole("button", { name: /Limit Graph/i }))
})
