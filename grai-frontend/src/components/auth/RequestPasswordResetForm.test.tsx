import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import RequestPasswordResetForm, {
  REQUEST_PASSWORD_RESET,
} from "./RequestPasswordResetForm"

test("submit", async () => {
  const user = userEvent.setup()

  render(<RequestPasswordResetForm />, {
    withRouter: true,
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /email/i }),
        "email@grai.io",
      ),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /submit/i })),
  )

  await screen.findByText("Password reset email sent")
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

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /email/i }),
        "email@grai.io",
      ),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /submit/i })),
  )

  await screen.findByText("Error!")
})
