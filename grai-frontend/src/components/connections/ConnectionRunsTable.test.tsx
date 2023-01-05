import { Table, TableBody } from "@mui/material"
import userEvent from "@testing-library/user-event"
import React from "react"
import { render, renderWithRouter, screen } from "testing"
import ConnectionProperties from "./ConnectionProperties"
import ConnectionRunsTable from "./ConnectionRunsTable"

const runs = [
  {
    id: "1",
    user: {
      id: "1",
      first_name: "user",
      last_name: "test",
    },
    status: "success",
    created_at: "1234",
    started_at: "1234",
    finished_at: null,
  },
]

test("renders", async () => {
  renderWithRouter(<ConnectionRunsTable runs={runs} />)
})

test("renders empty", async () => {
  renderWithRouter(<ConnectionRunsTable runs={[]} />)
})
