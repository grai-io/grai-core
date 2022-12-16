import userEvent from "@testing-library/user-event"
import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import ConnectionsTable from "./ConnectionsTable"

const connection = {
  id: "1",
  namespace: "namespace1",
  name: "connection 1",
  connector: {
    id: "1",
    name: "connector 1",
  },
}

test("renders", async () => {
  renderWithRouter(<ConnectionsTable connections={[connection]} />)
})

test("renders loading", async () => {
  renderWithRouter(<ConnectionsTable connections={[]} loading />)
})

test("renders empty", async () => {
  renderWithRouter(<ConnectionsTable connections={[]} />)
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = renderWithRouter(
    <ConnectionsTable connections={[connection]} />,
    {
      routes: ["/:nodeId"],
    }
  )

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})
