import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { CREATE_SOURCE } from "components/sources/CreateSource"
import SourceCreate, { GET_WORKSPACE } from "./SourceCreate"

test("renders", async () => {
  render(<SourceCreate />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Create Source")).toBeInTheDocument()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<SourceCreate />, {
    routes: ["/:organisationName/:workspaceName/sources/:sourceId"],
  })

  await waitFor(() => {
    expect(screen.getByText("Create Source")).toBeInTheDocument()
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "test-source",
      ),
  )

  await act(
    async () =>
      await user.type(
        screen.getByRole("spinbutton", { name: /priority/i }),
        "1",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
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
            name: "Workspace 1",
          },
        },
      },
    },
    {
      request: {
        query: CREATE_SOURCE,
        variables: {
          workspaceId: "1",
          name: "test-source",
          priority: 0,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<SourceCreate />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Create Source")).toBeInTheDocument()
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "test-source",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
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

  render(<SourceCreate />, { mocks, withRouter: true })

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

  render(<SourceCreate />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
