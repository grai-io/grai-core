import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import PasswordSettings, { UPDATE_PASSWORD } from "./PasswordSettings"

test("renders", async () => {
  renderWithRouter(<PasswordSettings />)

  expect(screen.getByText("Change Password")).toBeTruthy()
})

test("submit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<PasswordSettings />)

  expect(screen.getByText("Change Password")).toBeTruthy()

  await user.type(screen.getByTestId("current-password"), "password")
  await user.type(screen.getByTestId("new-password"), "password2")

  await user.click(screen.getByRole("button", { name: /save/i }))
})

test("error", async () => {
  const user = userEvent.setup()

  const mock = {
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
  }

  renderWithMocks(<PasswordSettings />, [mock])

  expect(screen.getByText("Change Password")).toBeTruthy()

  await user.type(screen.getByTestId("current-password"), "password")
  await user.type(screen.getByTestId("new-password"), "password2")

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
