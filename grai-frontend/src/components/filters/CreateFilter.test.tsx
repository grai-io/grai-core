import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import { input } from "testing/autocomplete"
import CreateFilter from "./CreateFilter"

test("renders", async () => {
  render(<CreateFilter workspaceId="1" tags={[]} />, {
    withRouter: true,
  })

  expect(screen.getByRole("textbox", { name: /name/i })).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateFilter workspaceId="1" tags={[]} />, {
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

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /add filter/i }))
  )

  input(screen.getByTestId("autocomplete-property"))
  input(screen.getByTestId("autocomplete-field"))
  input(screen.getByTestId("autocomplete-operator"))
  input(screen.getByTestId("autocomplete-value"), "t")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
