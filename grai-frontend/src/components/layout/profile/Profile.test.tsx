import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import Profile from "./Profile"

const profile = {
  id: "1",
  username: "test",
  first_name: "First",
  last_name: "Last",
}

test("renders", async () => {
  render(<Profile expanded profile={profile} />, {
    withRouter: true,
  })

  await screen.findByText("First Last")
})

test("renders collapsed", async () => {
  render(<Profile expanded={false} profile={profile} />, {
    withRouter: true,
  })

  await screen.findByText("FL")
})

const emptyProfile = {
  id: "1",
  username: "test",
  first_name: "",
  last_name: "",
}

test("renders empty", async () => {
  render(<Profile expanded profile={emptyProfile} />, {
    withRouter: true,
  })

  await screen.findByTestId("PersonOutlineIcon")

  expect(screen.getByText("Profile")).toBeTruthy()
})

test("renders empty collapsed", async () => {
  render(<Profile expanded={false} profile={emptyProfile} />, {
    withRouter: true,
  })

  await screen.findByTestId("PersonOutlineIcon")
})

test("renders no profile", async () => {
  render(<Profile expanded />, {
    withRouter: true,
  })

  await waitFor(() =>
    expect(screen.queryByText("Profile")).not.toBeInTheDocument(),
  )
})

test("logout", async () => {
  render(<Profile expanded profile={profile} />, {
    withRouter: true,
  })

  await screen.findByText("First Last")

  await act(async () => await userEvent.click(screen.getByText("First Last")))

  await screen.findByText("Logout")

  await act(async () => await userEvent.click(screen.getByText("Logout")))
})
