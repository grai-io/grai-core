import { render, screen, waitFor } from "testing"
import ConnectionCreateContent from "./ConnectionCreateContent"

const workspace = {
  id: "1",
}

test("renders", async () => {
  render(<ConnectionCreateContent workspace={workspace} />, {
    withRouter: true,
  })

  await waitFor(() =>
    expect(screen.queryAllByText("Select Integration")).toHaveLength(2),
  )

  await waitFor(() =>
    expect(screen.queryAllByText("Hello World")).toHaveLength(3),
  )
})

test("renders schedule", async () => {
  render(<ConnectionCreateContent workspace={workspace} />, {
    route: "/default/demo/connections/create?step=schedule&connectionId=1",
    path: "/:organisationName/:workspaceName/connections/create",
    withRouter: true,
  })

  await screen.findByText(/Schedule type/i)
})

test("renders schedule missing connectionId", async () => {
  render(<ConnectionCreateContent workspace={workspace} />, {
    route: "/default/demo/connections/create?step=schedule",
    path: "/:organisationName/:workspaceName/connections/create",
    withRouter: true,
  })

  await waitFor(() =>
    expect(screen.queryByText(/Schedule type/i)).not.toBeInTheDocument(),
  )

  expect(screen.getByText("Page not found")).toBeInTheDocument()
})

test("renders connection", async () => {
  render(<ConnectionCreateContent workspace={workspace} />, {
    route: "/default/demo/connections/create?connectionId=1",
    path: "/:organisationName/:workspaceName/connections/create",
    withRouter: true,
  })

  await screen.findByText("Invite a teammate")
})

test("renders connectorId", async () => {
  render(<ConnectionCreateContent workspace={workspace} />, {
    route: "/default/demo/connections/create?connectorId=1",
    path: "/:organisationName/:workspaceName/connections/create",
    withRouter: true,
  })

  await screen.findByText("Invite a teammate")
})
