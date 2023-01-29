import userEvent from "@testing-library/user-event"
import React from "react"
import { renderWithRouter, screen } from "testing"
import ConnectionsTable from "./ConnectionsTable"

const connections = [
  {
    id: "1",
    namespace: "namespace1",
    name: "connection 1",
    is_active: true,
    connector: {
      id: "1",
      name: "connector 1",
    },
    runs: [],
    last_run: null,
    last_successful_run: null,
  },
  {
    id: "2",
    namespace: "namespace1",
    name: "connection 2",
    is_active: false,
    connector: {
      id: "1",
      name: "connector 1",
    },
    runs: [],
    last_run: null,
    last_successful_run: null,
  },
]

test("renders", async () => {
  renderWithRouter(
    <ConnectionsTable connections={connections} workspaceId="1" />
  )
})

test("renders loading", async () => {
  renderWithRouter(
    <ConnectionsTable connections={[]} workspaceId="1" loading />
  )
})

test("renders empty", async () => {
  renderWithRouter(<ConnectionsTable connections={[]} workspaceId="1" />)

  expect(screen.getByText("No connections found")).toBeTruthy()
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = renderWithRouter(
    <ConnectionsTable connections={connections} workspaceId="1" />,
    {
      routes: ["/:nodeId"],
    }
  )

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeTruthy()
})
