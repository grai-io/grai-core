import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import RequestPasswordResetForm, {
  REQUEST_PASSWORD_RESET,
} from "./RequestPasswordResetForm"

test("submit", async () => {
  const user = userEvent.setup()

  render(<RequestPasswordResetForm />, {
    withRouter: true,
  })

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Password reset email sent")).toBeInTheDocument()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: REQUEST_PASSWORD_RESET,
        variables: {
          email: "email@grai.io",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<RequestPasswordResetForm />, { mocks })

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
