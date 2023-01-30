import React from "react"
import { render } from "testing"
import runPolling from "./runPolling"

const startPolling = jest.fn()
const stopPolling = jest.fn()

const TestComponent: React.FC<{ status: string }> = ({ status }) => {
  runPolling(status, startPolling, stopPolling)

  return null
}

test("runDuration queued", () => {
  render(<TestComponent status="queued" />)

  expect(startPolling).toHaveBeenCalled()
})

test("runDuration running", () => {
  render(<TestComponent status="running" />)

  expect(startPolling).toHaveBeenCalled()
})

test("runDuration success", () => {
  render(<TestComponent status="success" />)

  expect(stopPolling).toHaveBeenCalled()
})

test("runDuration error", () => {
  render(<TestComponent status="error" />)

  expect(stopPolling).toHaveBeenCalled()
})
