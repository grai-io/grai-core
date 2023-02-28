import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Home, { GET_WORKSPACE } from "./Home"
import Workspaces, { GET_WORKSPACES } from "./workspaces/Workspaces"

test("renders", async () => {
  render(<Home />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Welcome to Grai/i })
    ).toBeTruthy()
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
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

  render(<Home />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
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

  render(<Home />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("missing workspace", async () => {
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
        errors: [new GraphQLError("Can't find workspace")],
      },
    },
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        data: {
          workspaces: [],
        },
      },
    },
  ]

  render(<Home />, {
    routes: [
      {
        path: "/workspaces",
        element: <Workspaces />,
      },
    ],
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).toBeFalsy()
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Create a workspace/i })
    ).toBeInTheDocument()
  })
})
