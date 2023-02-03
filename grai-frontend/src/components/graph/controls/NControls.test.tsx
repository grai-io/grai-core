import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithRouter, screen } from "testing"
import { ReactFlowProvider } from "reactflow"
import NControls from "./NControls"

test("renders", async () => {
  let value = 1
  const setValue = (input: number) => (value = input)

  renderWithRouter(
    <ReactFlowProvider>
      <NControls
        options={{
          value,
          setValue,
        }}
      />
    </ReactFlowProvider>
  )

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()
})

test("plus", async () => {
  let value = 1
  const setValue = (input: number) => (value = input)

  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <NControls
        options={{
          value,
          setValue,
        }}
      />
    </ReactFlowProvider>
  )

  expect(value).toEqual(1)

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()

  await user.click(screen.getByTestId("AddIcon"))

  expect(value).toEqual(2)
})

test("minus", async () => {
  let value = 2
  const setValue = (input: number) => (value = input)

  const user = userEvent.setup()

  renderWithRouter(
    <ReactFlowProvider>
      <NControls
        options={{
          value,
          setValue,
        }}
      />
    </ReactFlowProvider>
  )

  expect(value).toEqual(2)

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()

  await user.click(screen.getByTestId("RemoveIcon"))

  expect(value).toEqual(1)
})
