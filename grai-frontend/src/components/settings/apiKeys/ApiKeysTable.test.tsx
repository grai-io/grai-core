import React from "react"
import { render, screen } from "testing"
import ApiKeysTable from "./ApiKeysTable"

const keys = [
  {
    id: "1",
    name: "key 1",
    prefix: "1234a",
    created: "2021-01-21",
    revoked: false,
    expiry_date: null,
    created_by: {
      id: "1",
      username: "edward",
    },
  },
  {
    id: "2",
    name: "key 2",
    prefix: "1234a",
    created: "2021-01-21",
    revoked: true,
    expiry_date: null,
    created_by: {
      id: "1",
      username: "edward",
    },
  },
]

test("renders", async () => {
  render(<ApiKeysTable keys={keys} />)

  expect(screen.getByText("key 1")).toBeInTheDocument()
})

test("loading", async () => {
  render(<ApiKeysTable keys={[]} loading />)

  expect(screen.getByRole("progressbar")).toBeTruthy()
})

test("empty", async () => {
  render(<ApiKeysTable keys={[]} />)

  expect(screen.getByText("No API keys found")).toBeInTheDocument()
})
