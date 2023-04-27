import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import CreateFilter from "./CreateFilter"

test("renders", async () => {
  render(<CreateFilter workspaceId="1" />, {
    withRouter: true,
  })

  expect(screen.getByRole("textbox", { name: /name/i })).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateFilter workspaceId="1" />, {
    withRouter: true,
    routes: ["/:organisationName/:workspaceName/filters/:filterId"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter"
      )
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /add filter/i }))
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
