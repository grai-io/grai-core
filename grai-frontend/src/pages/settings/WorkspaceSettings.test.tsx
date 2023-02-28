import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import { UPDATE_WORKSPACE } from "components/settings/workspace/WorkspaceForm"
import WorkspaceSettings, { GET_WORKSPACE } from "./WorkspaceSettings"

test("renders", async () => {
  render(<WorkspaceSettings />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Workspace Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Hello World")
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceSettings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Workspace Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<WorkspaceSettings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Workspace Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<WorkspaceSettings />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Workspace Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Hello World")
  })

  await user.type(screen.getByRole("textbox", { name: /name/i }), "Workspace 1")

  await user.click(screen.getByRole("button", { name: /save/i }))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            name: "Test Workspace",
          },
        },
      },
    },
    {
      request: {
        query: UPDATE_WORKSPACE,
        variables: {
          id: "1",
          name: "Test Workspace",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceSettings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Workspace Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Test Workspace")
  })

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
