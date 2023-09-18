import userEvent from "@testing-library/user-event"
import { LOGIN } from "./LoginForm"
import { act, render, screen, waitFor } from "testing"
import LoginWrapper from "./LoginWrapper"

test("submit required 2fa", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: LOGIN,
        variables: {
          username: "email@grai.io",
          password: "password",
        },
      },
      result: {
        data: {
          login: {
            data: [
              {
                id: "1",
                name: "",
                __typename: "DeviceData",
              },
            ],
            __typename: "DeviceDataWrapper",
          },
        },
      },
    },
  ]

  render(<LoginWrapper />, {
    guestRoute: true,
    loggedIn: false,
    path: "/login",
    route: "/login",
    routes: ["/"],
    mocks,
  })

  await act(
    async () => await user.type(screen.getByTestId("email"), "email@grai.io"),
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password"),
  )

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /log in/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Two Factor Authentication")).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /back/i })),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /back/i })),
  )
})
