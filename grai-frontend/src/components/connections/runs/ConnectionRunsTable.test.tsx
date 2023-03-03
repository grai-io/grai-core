import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
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
  render(<ConnectionRunsTable runs={runs} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
})

test("renders empty", async () => {
  render(<ConnectionRunsTable runs={[]} />, {
    withRouter: true,
  })

  expect(screen.getByText("No runs found")).toBeInTheDocument()
})

test("row click", async () => {
  const user = userEvent.setup()

  const { container } = render(<ConnectionRunsTable runs={runs} />, {
    routes: ["/:organisationName/:workspaceName/runs/:runId"],
  })

  expect(screen.getByText("Success")).toBeInTheDocument()

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0])
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
