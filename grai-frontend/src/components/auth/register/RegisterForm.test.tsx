import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import RegisterForm, { REGISTER } from "./RegisterForm"

test("renders", async () => {
  const user = userEvent.setup()

  render(<RegisterForm />, {
    guestRoute: true,
    loggedIn: false,
    path: "/register",
    route: "/register",
    routes: ["/"],
  })

  await act(
    async () => await user.type(screen.getByTestId("name"), "Test User"),
  )
  await act(
    async () => await user.type(screen.getByTestId("email"), "email@grai.io"),
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password"),
  )

  await waitFor(() =>
    expect(screen.getByTestId("password")).toHaveValue("password"),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /get started/i })),
  )

  await screen.findByText("New Page")
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: REGISTER,
        variables: {
          name: "Test User",
          username: "email@grai.io",
          password: "password",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<RegisterForm />, {
    withRouter: true,
    mocks,
  })

  await act(
    async () => await user.type(screen.getByTestId("name"), "Test User"),
  )
  await act(
    async () => await user.type(screen.getByTestId("email"), "email@grai.io"),
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password"),
  )

  await waitFor(() =>
    expect(screen.getByTestId("password")).toHaveValue("password"),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /get started/i })),
  )

  await screen.findByText("Error!")
})
