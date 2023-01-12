import userEvent from "@testing-library/user-event"
import React from "react"
import { renderWithRouter, screen } from "testing"
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

  expect(screen.getByText("Success")).toBeTruthy()
})

test("renders empty", async () => {
  renderWithRouter(<ConnectionRunsTable runs={[]} />)

  expect(screen.getByText("No runs found")).toBeTruthy()
})

test("row click", async () => {
  const user = userEvent.setup()

  const { container } = renderWithRouter(<ConnectionRunsTable runs={runs} />, {
    routes: ["/workspaces/:workspaceId/runs/:runId"],
  })

  expect(screen.getByText("Success")).toBeTruthy()

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeTruthy()
})
