import userEvent from "@testing-library/user-event"
import { UPDATE_WORKSPACE } from "components/settings/workspace/WorkspaceForm"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import WorkspaceSettings, { GET_WORKSPACE } from "./WorkspaceSettings"

test("renders", async () => {
  renderWithRouter(<WorkspaceSettings />)

  await waitFor(() => {
    screen.getByText("Workspace Settings")
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Hello World")
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_WORKSPACE,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<WorkspaceSettings />, [mock])

  await waitFor(() => {
    screen.getByText("Workspace Settings")
  })

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("not found", async () => {
  const mock = {
    request: {
      query: GET_WORKSPACE,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      data: {
        workspace: null,
      },
    },
  }

  renderWithMocks(<WorkspaceSettings />, [mock])

  await waitFor(() => {
    screen.getByText("Workspace Settings")
  })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  renderWithRouter(<WorkspaceSettings />)

  await waitFor(() => {
    screen.getByText("Workspace Settings")
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
          workspaceId: "",
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

  renderWithMocks(<WorkspaceSettings />, mocks)

  await waitFor(() => {
    screen.getByText("Workspace Settings")
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Test Workspace")
  })

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
