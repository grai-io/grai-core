import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import RunsTable from "./RunsTable"

const runs = [
  {
    id: "1",
    connection: {
      id: "1",
      name: "Connection 1",
      connector: {
        id: "1",
        name: "Connector 1",
      },
    },
    status: "success",
    created_at: "1",
    started_at: null,
    finished_at: null,
    user: {
      id: "1",
      first_name: "firstname",
      last_name: "lastname",
    },
  },
]

test("renders", async () => {
  render(<RunsTable runs={runs} />, {
    withRouter: true,
  })

  expect(screen.getByText("Connection 1")).toBeInTheDocument()
  expect(screen.getByText("Connector 1")).toBeInTheDocument()
  expect(screen.getByText("firstname")).toBeInTheDocument()
})

test("loading", async () => {
  render(<RunsTable runs={[]} loading />, {
    withRouter: true,
  })

  expect(screen.getByRole("progressbar")).toBeInTheDocument()
})

test("empty", async () => {
  render(<RunsTable runs={[]} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("No runs found")).toBeInTheDocument()
  })
})

test("row click", async () => {
  const user = userEvent.setup()

  const { container } = render(<RunsTable runs={runs} />, {
    routes: ["/:runId"],
  })

  expect(screen.getByText("Success")).toBeInTheDocument()

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
