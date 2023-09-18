import userEvent from "@testing-library/user-event"
import TokenForm, { LOGIN } from "./TokenForm"
import { act, render, screen, waitFor } from "testing"
import { GraphQLError } from "graphql"

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

  await waitFor(() =>
    expect(screen.getByText("Two Factor Authentication")).toBeInTheDocument(),
  )

  await waitFor(() =>
    expect(screen.getByText("Select a device")).toBeInTheDocument(),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /test/i })),
  )

  await waitFor(() =>
    expect(
      screen.getByText("Please enter the 6 digit code from your device"),
    ).toBeInTheDocument(),
  )

  await act(async () => await user.type(screen.getByRole("textbox"), "123456"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
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

  await waitFor(() =>
    expect(screen.getByText("Two Factor Authentication")).toBeInTheDocument(),
  )

  await waitFor(() =>
    expect(
      screen.getByText("Please enter the 6 digit code from your device"),
    ).toBeInTheDocument(),
  )

  await act(async () => await user.type(screen.getByRole("textbox"), "123456"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
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

  await waitFor(() =>
    expect(screen.getByText("Two Factor Authentication")).toBeInTheDocument(),
  )

  await waitFor(() =>
    expect(
      screen.getByText("Please enter the 6 digit code from your device"),
    ).toBeInTheDocument(),
  )

  await act(async () => await user.type(screen.getByRole("textbox"), "123456"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
