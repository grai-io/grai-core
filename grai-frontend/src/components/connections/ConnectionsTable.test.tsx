import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen } from "testing"
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
  render(<ConnectionsTable connections={connections} workspaceId="1" />, {
    withRouter: true,
  })
})

test("renders loading", async () => {
  render(<ConnectionsTable connections={[]} workspaceId="1" loading />, {
    withRouter: true,
  })
})

test("renders empty", async () => {
  render(<ConnectionsTable connections={[]} workspaceId="1" />, {
    withRouter: true,
  })

  expect(screen.getByText("No connections found")).toBeInTheDocument()
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(
    <ConnectionsTable connections={connections} workspaceId="1" />,
    {
      routes: ["/:nodeId"],
    }
  )

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
