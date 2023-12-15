import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import CreateDeviceForm, { CREATE_DEVICE } from "./CreateDeviceForm"

const defaultProps = {
  onClose: jest.fn(),
}

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateDeviceForm {...defaultProps} />)

  await screen.findByText("Scan the qr code with an authenticator app")

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /next/i }))
  })

  await screen.findByText("Enter a code from your authenticator")

  await act(async () => {
    await user.type(screen.getByRole("textbox"), "123456")
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /continue/i }))
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: CREATE_DEVICE,
        variables: {
          name: "TOTP",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CreateDeviceForm {...defaultProps} />, { mocks })

  await screen.findByText("Error!")
})

test("back", async () => {
  const user = userEvent.setup()

  render(<CreateDeviceForm {...defaultProps} />)

  await screen.findByText("Scan the qr code with an authenticator app")

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /next/i }))
  })

  await screen.findByText("Enter a code from your authenticator")

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /back/i }))
  })

  await screen.findByText("Scan the qr code with an authenticator app")
})
