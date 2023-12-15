import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import MembershipsHeader from "./MembershipsHeader"

test("renders", async () => {
  render(<MembershipsHeader workspaceId="1" />, {
    withRouter: true,
  })

  await screen.findByText("Memberships")
})

test("open", async () => {
  const user = userEvent.setup()

  render(<MembershipsHeader workspaceId="1" />, {
    withRouter: true,
  })

  await screen.findByText("Memberships")

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Invite user/i })),
  )

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))
})
