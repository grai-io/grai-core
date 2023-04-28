import React from "react"
import { render, screen } from "testing"
import RunLog from "./RunLog"

test("renders", async () => {
  const run = {
    id: "1",
    metadata: {
      error: "A useful error",
    },
  }

  render(<RunLog run={run} />)

  expect(screen.getByText("A useful error")).toBeInTheDocument()
})

test("renders no errors", async () => {
  const run = {
    id: "1",
    metadata: {},
  }

  render(<RunLog run={run} />)

  expect(screen.queryByText("Error")).not.toBeInTheDocument()
})
