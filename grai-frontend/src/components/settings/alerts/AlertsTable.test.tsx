import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import AlertsTable from "./AlertsTable"

const alerts = [
  {
    id: "1",
    name: "Test Alert",
    channel: "email",
    channel_metadata: {},
    triggers: {},
    is_active: true,
    created_at: "1",
  },
  {
    id: "2",
    name: "Test Alert2",
    channel: "email",
    channel_metadata: {},
    triggers: {},
    is_active: false,
    created_at: "1",
  },
]

test("renders", async () => {
  render(<AlertsTable alerts={alerts} />, {
    withRouter: true,
  })

  expect(screen.getByText("Test Alert")).toBeInTheDocument()
})

test("empty", async () => {
  render(<AlertsTable alerts={[]} />, {
    withRouter: true,
  })

  expect(screen.getByText("No alerts found")).toBeInTheDocument()
})

test("loading", async () => {
  render(<AlertsTable alerts={[]} loading />, {
    withRouter: true,
  })

  expect(screen.getByRole("progressbar")).toBeTruthy()
})

test("row click", async () => {
  const user = userEvent.setup()

  const { container } = render(<AlertsTable alerts={alerts} />, {
    routes: ["/:organisationName/:workspaceName/settings/alerts/:alertId"],
  })

  expect(screen.getByText("Test Alert")).toBeInTheDocument()

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0]),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
