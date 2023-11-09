import { render, screen } from "testing"
import AppDrawerItem from "./AppDrawerItem"

test("renders", async () => {
  render(
    <AppDrawerItem
      title="test"
      path="/"
      icon={<>Test Icon</>}
      expand={false}
    />,
    { withRouter: true },
  )

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.queryByText("test")).not.toBeInTheDocument()
})

test("renders expanded", async () => {
  render(<AppDrawerItem title="test" path="/" icon={<>Test Icon</>} expand />, {
    withRouter: true,
  })

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.getByText("test")).toBeInTheDocument()
})

test("alert", async () => {
  render(
    <AppDrawerItem
      title="test"
      path="/"
      icon={<>Test Icon</>}
      expand={false}
      alert
    />,
    { withRouter: true },
  )

  expect(screen.getByText("Test Icon")).toBeInTheDocument()
  expect(screen.queryByText("test")).not.toBeInTheDocument()
  expect(screen.getByTestId("app-drawer-item-alert")).toBeInTheDocument()
})
