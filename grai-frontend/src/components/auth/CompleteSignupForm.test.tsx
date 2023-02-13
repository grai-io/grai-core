import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, waitFor } from "testing"
import { GraphQLError } from "graphql"
import CompleteSignupForm, { COMPLETE_SIGNUP } from "./CompleteSignupForm"

test("submit", async () => {
  const user = userEvent.setup()

  render(<CompleteSignupForm />, {
    route: "?token=abc&uid=1234",
    path: "/",
  })

  await user.type(screen.getByRole("textbox", { name: /first name/i }), "test")
  await user.type(screen.getByRole("textbox", { name: /last name/i }), "user")
  await user.type(screen.getByTestId("password"), "password")

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(
      screen.getByText(
        "You are all signed up, please login to view your workspace."
      )
    ).toBeTruthy()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: COMPLETE_SIGNUP,
        variables: {
          token: "abc",
          uid: "1234",
          first_name: "test",
          last_name: "user",
          password: "password",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CompleteSignupForm />, {
    route: "?token=abc&uid=1234",
    path: "/",
    mocks,
  })

  await user.type(screen.getByRole("textbox", { name: /first name/i }), "test")
  await user.type(screen.getByRole("textbox", { name: /last name/i }), "user")
  await user.type(screen.getByTestId("password"), "password")

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
