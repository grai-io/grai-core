import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor, within } from "testing"
import EditMembershipDialog, { UPDATE_MEMBERSHIP } from "./EditMembershipDialog"

const membership = {
  id: "1",
  role: "member",
  is_active: true,
  user: {
    first_name: "Test",
    last_name: "User",
    username: "test@example.com",
  },
}

test("renders", async () => {
  render(
    <EditMembershipDialog
      membership={membership}
      open={true}
      onClose={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  await waitFor(() => {
    expect(screen.getByText("Edit Membership")).toBeInTheDocument()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(
    <EditMembershipDialog
      membership={membership}
      open={true}
      onClose={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  await waitFor(() => {
    expect(screen.getByText("Edit Membership")).toBeInTheDocument()
  })

  fireEvent.change(screen.getByTestId("role-select"), {
    target: { value: "admin" },
  })

  await act(async () => {
    user.click(screen.getByRole("checkbox", { name: /Active/i }))
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i }))
  )
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_MEMBERSHIP,
        variables: {
          id: "1",
          role: "admin",
          is_active: true,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <EditMembershipDialog
      membership={membership}
      open={true}
      onClose={() => {}}
    />,
    { mocks }
  )

  await waitFor(() => {
    expect(screen.getByText("Edit Membership")).toBeInTheDocument()
  })

  fireEvent.change(screen.getByTestId("role-select"), {
    target: { value: "admin" },
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
