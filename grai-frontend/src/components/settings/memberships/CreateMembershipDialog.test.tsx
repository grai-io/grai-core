import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import CreateMembershipDialog, {
  CREATE_MEMBERSHIP,
} from "./CreateMembershipDialog"

test("renders", async () => {
  render(
    <CreateMembershipDialog workspaceId="1" open={true} onClose={() => {}} />,
    {
      withRouter: true,
    }
  )

  await waitFor(() => {
    expect(screen.getByText("Invite users")).toBeInTheDocument()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(
    <CreateMembershipDialog workspaceId="1" open={true} onClose={() => {}} />,
    {
      withRouter: true,
    }
  )

  await waitFor(() => {
    expect(screen.getByText("Invite users")).toBeInTheDocument()
  })

  await act(
    async () => await user.type(screen.getByRole("textbox"), "email@grai.io")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i }))
  )
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_MEMBERSHIP,
        variables: {
          role: "member",
          email: "email@grai.io",
          workspaceId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <CreateMembershipDialog workspaceId="1" open={true} onClose={() => {}} />,
    { mocks }
  )

  await waitFor(() => {
    expect(screen.getByText("Invite users")).toBeInTheDocument()
  })

  await act(
    async () => await user.type(screen.getByRole("textbox"), "email@grai.io")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
