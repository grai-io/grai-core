import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import MembershipsHeader from "./MembershipsHeader"

test("renders", async () => {
  render(<MembershipsHeader workspaceId="1" />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })
})

test("open", async () => {
  const user = userEvent.setup()

  render(<MembershipsHeader workspaceId="1" />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Invite user/i })),
  )

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))
})
