import React from "react"
import { render, screen } from "testing"
import RunHeader from "./RunHeader"

test("renders", async () => {
  const run = {
    id: "123456789",
    status: "success",
    connector: {
      id: "1",
      name: "Connector",
    },
    connection: null,
  }

  render(<RunHeader run={run} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
  expect(screen.getByText("123456")).toBeInTheDocument()
})

test("renders connection", async () => {
  const run = {
    id: "123456789",
    status: "success",
    connector: {
      id: "1",
      name: "Connector",
    },
    connection: {
      id: "2",
      name: "Connection1",
    },
  }

  render(<RunHeader run={run} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
  expect(screen.getByText("Connection1/123456")).toBeInTheDocument()
})
