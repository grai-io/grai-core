import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { CREATE_WORKSPACE } from "components/workspaces/WorkspaceForm"
import { act, render, screen, waitFor } from "testing"
import WorkspaceCreate from "./WorkspaceCreate"

test("renders", async () => {
  render(<WorkspaceCreate />, {
    route: "/workspaces/create?organisationId=1",
    path: "/workspaces/create",
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Create a workspace/i })
    ).toBeInTheDocument()
  })
})

test("renders no organisation", async () => {
  render(<WorkspaceCreate />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Create a workspace/i })
    ).toBeInTheDocument()
  })

  expect(screen.getByText("No organisationId found")).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<WorkspaceCreate />, {
    route: "/workspaces/create?organisationId=1",
    path: "/workspaces/create",
    withRouter: true,
    routes: ["/Hello World/Hello World"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestWorkspace"
      )
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_WORKSPACE,
        variables: {
          name: "TestWorkspace",
          organisationId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceCreate />, {
    route: "/workspaces/create?organisationId=1",
    path: "/workspaces/create",
    withRouter: true,
    mocks,
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestWorkspace"
      )
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
