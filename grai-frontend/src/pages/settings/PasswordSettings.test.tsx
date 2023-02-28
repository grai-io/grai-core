import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import PasswordSettings, { UPDATE_PASSWORD } from "./PasswordSettings"

test("renders", async () => {
  render(<PasswordSettings />, {
    withRouter: true,
  })

  expect(screen.getByText("Change Password")).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<PasswordSettings />, {
    withRouter: true,
  })

  expect(screen.getByText("Change Password")).toBeInTheDocument()

  await user.type(screen.getByTestId("current-password"), "password")
  await user.type(screen.getByTestId("new-password"), "password2")

  await user.click(screen.getByRole("button", { name: /save/i }))
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_PASSWORD,
        variables: {
          old_password: "password",
          password: "password2",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<PasswordSettings />, { mocks, withRouter: true })

  expect(screen.getByText("Change Password")).toBeInTheDocument()

  await user.type(screen.getByTestId("current-password"), "password")
  await user.type(screen.getByTestId("new-password"), "password2")

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
