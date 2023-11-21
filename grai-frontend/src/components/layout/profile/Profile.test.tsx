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

  await waitFor(() => {
    expect(screen.getByText("First Last")).toBeTruthy()
  })
})

test("renders collapsed", async () => {
  render(<Profile expanded={false} profile={profile} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("FL")).toBeTruthy()
  })
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

  await waitFor(() => {
    expect(screen.getByTestId("PersonOutlineIcon")).toBeTruthy()
  })

  expect(screen.getByText("Profile")).toBeTruthy()
})

test("renders empty collapsed", async () => {
  render(<Profile expanded={false} profile={emptyProfile} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByTestId("PersonOutlineIcon")).toBeTruthy()
  })
})

test("renders no profile", async () => {
  render(<Profile expanded />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.queryByText("Profile")).not.toBeInTheDocument()
  })
})

test("logout", async () => {
  render(<Profile expanded profile={profile} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("First Last")).toBeTruthy()
  })

  await act(async () => await userEvent.click(screen.getByText("First Last")))

  await waitFor(() => {
    expect(screen.getByText("Logout")).toBeInTheDocument()
  })

  await act(async () => await userEvent.click(screen.getByText("Logout")))
})
