import { render, screen } from "testing"
import AppDrawerItem from "./AppDrawerItem"

const page = {
  title: "test",
  path: "/",
  icon: <>Test Icon</>,
}

test("renders", async () => {
  render(<AppDrawerItem page={page} expanded={false} />, { withRouter: true })

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.queryByText("test")).not.toBeInTheDocument()
})

test("renders expanded", async () => {
  render(<AppDrawerItem page={page} expanded />, {
    withRouter: true,
  })

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.getByText("test")).toBeInTheDocument()
})

test("alert", async () => {
  render(<AppDrawerItem page={{ ...page, alert: true }} expanded={false} />, {
    withRouter: true,
  })

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.queryByText("test")).not.toBeInTheDocument()
  expect(screen.getByTestId("app-drawer-item-alert")).toBeInTheDocument()
})

test("renders selected", async () => {
  render(<AppDrawerItem page={{ ...page, path: "test" }} expanded />, {
    withRouter: true,
    route: "/default/demo/test",
    path: "/:organisationName/:workspaceName/test",
  })

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.getByText("test")).toBeInTheDocument()
})
