import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import RequestPasswordResetForm, {
  REQUEST_PASSWORD_RESET,
} from "./RequestPasswordResetForm"
import { GraphQLError } from "graphql"

test("submit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<RequestPasswordResetForm />)

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getByText("Password reset email sent")).toBeTruthy()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mock = {
    request: {
      query: REQUEST_PASSWORD_RESET,
      variables: {
        email: "email@grai.io",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<RequestPasswordResetForm />, [mock])

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )

  await user.click(screen.getByRole("button", { name: /submit/i }))

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
