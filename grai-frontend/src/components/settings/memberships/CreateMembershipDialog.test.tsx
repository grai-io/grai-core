import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import CreateMembershipDialog, {
  CREATE_MEMBERSHIP,
} from "./CreateMembershipDialog"

test("renders", async () => {
  renderWithRouter(<CreateMembershipDialog open={true} onClose={() => {}} />)

  await waitFor(() => {
    expect(screen.getByText("Invite user")).toBeTruthy()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<CreateMembershipDialog open={true} onClose={() => {}} />)

  await waitFor(() => {
    expect(screen.getByText("Invite user")).toBeTruthy()
  })

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )

  await user.click(screen.getByRole("button", { name: /Save/i }))
})

test("error", async () => {
  const user = userEvent.setup()

  const mock = {
    request: {
      query: CREATE_MEMBERSHIP,
      variables: {
        role: "admin",
        email: "email@grai.io",
        workspaceId: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<CreateMembershipDialog open={true} onClose={() => {}} />, [
    mock,
  ])

  await waitFor(() => {
    expect(screen.getByText("Invite user")).toBeTruthy()
  })

  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "email@grai.io"
  )

  await user.click(screen.getByRole("button", { name: /Save/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})
