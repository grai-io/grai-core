import React from "react"
import { render, screen } from "testing"
import RunHeader from "./RunHeader"

test("renders", async () => {
  const run = {
    id: "123456789",
    status: "success",
    connection: null,
  }

  render(<RunHeader run={run} workspaceId="1" />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
  expect(screen.getByText("123456")).toBeInTheDocument()
})

test("renders connection", async () => {
  const run = {
    id: "123456789",
    status: "success",
    connection: {
      id: "2",
      name: "Connection1",
      last_run: null,
      last_successful_run: null,
      runs: [],
      connector: {
        id: "1",
        name: "Connector",
      },
    },
  }

  render(<RunHeader run={run} workspaceId="1" />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
  expect(screen.getByText("Connection1/123456")).toBeInTheDocument()
})
