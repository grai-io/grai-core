import React from "react"
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
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "Test User"
      )
  )
  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /email/i }),
        "email@grai.io"
      )
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password")
  )

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /register/i }))
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
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "Test User"
      )
  )
  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /email/i }),
        "email@grai.io"
      )
  )
  await act(
    async () => await user.type(screen.getByTestId("password"), "password")
  )

  await waitFor(() => {
    expect(screen.getByTestId("password")).toHaveValue("password")
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /register/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
