import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithRouter, screen } from "testing"
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

  renderWithRouter(<RunHeader run={run} />)

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

  renderWithRouter(<RunHeader run={run} />)

  expect(screen.getByText("Success")).toBeInTheDocument()
  expect(screen.getByText("Connection1/123456")).toBeInTheDocument()
})
