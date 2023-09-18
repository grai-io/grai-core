import { act, render, screen, waitFor } from "testing"
import Test, { CONFIRM_DEVICE } from "./Test"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"

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

  await waitFor(() =>
    expect(
      screen.getByText("Enter a code from your authenticator"),
    ).toBeInTheDocument(),
  )

  await act(async () => {
    await user.type(screen.getByRole("textbox"), "123456")
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /continue/i }))
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
