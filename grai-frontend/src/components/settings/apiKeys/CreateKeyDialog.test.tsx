import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor } from "testing"
import CreateKeyDialog, { CREATE_API_KEY } from "./CreateKeyDialog"

test("renders", async () => {
  render(<CreateKeyDialog workspaceId="1" open={false} onClose={() => {}} />)
})

test("renders open", async () => {
  render(<CreateKeyDialog workspaceId="1" open={true} onClose={() => {}} />)
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateKeyDialog workspaceId="1" open={true} onClose={() => {}} />)

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /name/i }), "key 3")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("API key created")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  expect(screen.queryByText("API key created")).toBeFalsy()
})

test("submit custom expiry date", async () => {
  const user = userEvent.setup()

  render(<CreateKeyDialog workspaceId="1" open={true} onClose={() => {}} />)

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /name/i }), "key 3")
  )

  fireEvent.change(screen.getByTestId("expiration-select"), {
    target: { value: "custom" },
  })

  await act(
    async () => await user.type(screen.getByTestId("date-input"), "01/01/2022")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("API key created")).toBeInTheDocument()
  })

  await act(async () => await user.click(screen.getByTestId("CloseIcon")))

  expect(screen.queryByText("API key created")).toBeFalsy()
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_API_KEY,
        variables: {
          name: "key 4",
          workspaceId: "1",
          expiry_date: null,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CreateKeyDialog workspaceId="1" open={true} onClose={() => {}} />, {
    mocks,
  })

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /name/i }), "key 4")
  )

  fireEvent.change(screen.getByTestId("expiration-select"), {
    target: { value: "none" },
  })

  await waitFor(() => {
    expect(screen.getByText("No expiration")).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
