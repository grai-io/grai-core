import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import CreateDeviceForm, { CREATE_DEVICE } from "./CreateDeviceForm"
import { GraphQLError } from "graphql"

const defaultProps = {
  onClose: jest.fn(),
}

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateDeviceForm {...defaultProps} />)

  await waitFor(() => {
    expect(
      screen.getByText("Scan the qr code with an authenticator app"),
    ).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /next/i }))
  })

  await waitFor(() => {
    expect(
      screen.getByText("Enter a code from your authenticator"),
    ).toBeInTheDocument()
  })

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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("back", async () => {
  const user = userEvent.setup()

  render(<CreateDeviceForm {...defaultProps} />)

  await waitFor(() => {
    expect(
      screen.getByText("Scan the qr code with an authenticator app"),
    ).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /next/i }))
  })

  await waitFor(() => {
    expect(
      screen.getByText("Enter a code from your authenticator"),
    ).toBeInTheDocument()
  })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /back/i }))
  })

  await waitFor(() => {
    expect(
      screen.getByText("Scan the qr code with an authenticator app"),
    ).toBeInTheDocument()
  })
})
