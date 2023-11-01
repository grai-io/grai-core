import React from "react"
import { render, screen } from "testing"
import ConnectionStatus from "./ConnectionStatus"

test("renders", async () => {
  const connection = {
    validated: true,
    last_run: null,
    connector: {
      name: "test",
      icon: null,
    },
  }

  render(<ConnectionStatus connection={connection} />)

  expect(screen.queryByText("Setup Incomplete")).not.toBeInTheDocument()
})

test("renders not validated", async () => {
  const connection = {
    validated: false,
    last_run: null,
    connector: {
      name: "test",
      icon: null,
    },
  }

  render(<ConnectionStatus connection={connection} />)

  expect(screen.getByText("Setup Incomplete")).toBeInTheDocument()
})
