import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
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
      events: true,
    },
    runs: { data: [] },
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
      events: false,
    },
    runs: { data: [] },
    last_run: null,
    last_successful_run: null,
  },
]

test("renders", async () => {
  render(
    <ConnectionsTable connections={connections} workspaceId="1" total={0} />,
    {
      withRouter: true,
    }
  )
})

test("renders loading", async () => {
  render(
    <ConnectionsTable connections={[]} workspaceId="1" loading total={0} />,
    {
      withRouter: true,
    }
  )
})

test("renders empty", async () => {
  render(<ConnectionsTable connections={[]} workspaceId="1" total={0} />, {
    withRouter: true,
  })

  expect(screen.getByText("No connections found")).toBeInTheDocument()
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(
    <ConnectionsTable connections={connections} workspaceId="1" total={0} />,
    {
      routes: ["/:nodeId"],
    }
  )

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0])
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
