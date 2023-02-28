import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
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

  await user.type(screen.getByRole("textbox", { name: /name/i }), "key 3")

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getByText("API key created")).toBeInTheDocument()
  })

  await user.click(screen.getByTestId("CloseIcon"))

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

  await user.type(screen.getByRole("textbox", { name: /name/i }), "key 4")

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
