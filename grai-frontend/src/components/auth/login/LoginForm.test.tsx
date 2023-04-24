import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import LoginForm, { LOGIN } from "./LoginForm"

test("submit", async () => {
  const user = userEvent.setup()

  render(<LoginForm />, {
    guestRoute: true,
    loggedIn: false,
    path: "/login",
    route: "/login",
    routes: ["/"],
  })

  await act(
    async () => await user.type(screen.getByTestId("email"), "email@grai.io")
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password")
  )

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /log in/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("error", async () => {
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
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<LoginForm />, {
    withRouter: true,
    mocks,
  })

  await act(
    async () => await user.type(screen.getByTestId("email"), "email@grai.io")
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password")
  )

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /log in/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
