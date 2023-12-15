import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import Test, { CONFIRM_DEVICE } from "./Test"

test("submit test error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CONFIRM_DEVICE,
        variables: {
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
    <Test
      device={{
        id: "1",
      }}
      onBack={jest.fn()}
      onClose={jest.fn()}
    />,
    { mocks },
  )

  await screen.findByText("Enter a code from your authenticator")

  await act(async () => {
    await user.type(screen.getByRole("textbox"), "123456")
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /continue/i }))
  })

  await screen.findByText("Error!")
})
