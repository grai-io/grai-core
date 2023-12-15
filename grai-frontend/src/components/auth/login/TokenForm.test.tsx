import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import TokenForm, { LOGIN } from "./TokenForm"

const onBack = jest.fn()

const defaultProps = {
  username: "email@grai.io",
  password: "password",
  devices: [
    {
      id: "1",
      name: "test",
    },
    {
      id: "2",
      name: "another device",
    },
  ],
  onBack,
}

test("submit multiple devices", async () => {
  const user = userEvent.setup()

  render(<TokenForm {...defaultProps} />, {
    guestRoute: true,
    loggedIn: false,
    path: "/login",
    route: "/login",
    routes: ["/"],
  })

  await screen.findByText("Two Factor Authentication")

  await screen.findByText("Select a device")

  await act(
    async () => await user.click(screen.getByRole("button", { name: /test/i })),
  )

  await screen.findByText("Please enter the 6 digit code from your device")

  await act(async () => await user.type(screen.getByRole("textbox"), "123456"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await screen.findByText("New Page")
})

test("submit single device", async () => {
  const user = userEvent.setup()

  render(
    <TokenForm
      {...defaultProps}
      devices={[
        {
          id: "1",
          name: "test",
        },
      ]}
    />,
    {
      guestRoute: true,
      loggedIn: false,
      path: "/login",
      route: "/login",
      routes: ["/"],
    },
  )

  await screen.findByText("Two Factor Authentication")

  await screen.findByText("Please enter the 6 digit code from your device")

  await act(async () => await user.type(screen.getByRole("textbox"), "123456"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await screen.findByText("New Page")
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: LOGIN,
        variables: {
          username: "email@grai.io",
          password: "password",
          deviceId: "1",
          token: "123456",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <TokenForm
      {...defaultProps}
      devices={[
        {
          id: "1",
          name: "test",
        },
      ]}
    />,
    {
      guestRoute: true,
      loggedIn: false,
      path: "/login",
      route: "/login",
      routes: ["/"],
      mocks,
    },
  )

  await screen.findByText("Two Factor Authentication")

  await screen.findByText("Please enter the 6 digit code from your device")

  await act(async () => await user.type(screen.getByRole("textbox"), "123456"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await screen.findByText("Error!")
})
