import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import { DELETE_CONNECTION } from "components/connections/ConnectionDelete"
import Connections, { GET_CONNECTIONS } from "./Connections"

test("renders", async () => {
  render(<Connections />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Connections />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByTestId("connection-refresh"))
  )

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

const connectionMock = {
  request: {
    query: GET_CONNECTIONS,
    variables: {
      organisationName: "",
      workspaceName: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        connections: [
          {
            id: "1",
            namespace: "default",
            name: "Connection 1",
            is_active: true,
            connector: {
              id: "1",
              name: "Connector 1",
            },
            runs: [],
            last_run: null,
            last_successful_run: null,
          },
        ],
      },
    },
  },
}

test("delete", async () => {
  const user = userEvent.setup()

  const mocks = [
    profileMock,
    connectionMock,
    {
      request: {
        query: DELETE_CONNECTION,
        variables: {
          id: "1",
        },
      },
      result: {
        data: {
          deleteConnection: {
            id: "1",
          },
        },
      },
    },
  ]

  render(<Connections />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })

  await act(async () => {
    await user.click(screen.getByTestId("MoreHorizIcon"))
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )
})

test("cancel delete", async () => {
  const user = userEvent.setup()

  const mocks = [
    profileMock,
    connectionMock,
    {
      request: {
        query: DELETE_CONNECTION,
        variables: {
          id: "1",
        },
      },
      result: {
        data: {
          deleteConnection: {
            id: "1",
          },
        },
      },
    },
  ]

  render(<Connections />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })

  await act(async () => {
    await user.click(screen.getByTestId("MoreHorizIcon"))
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /cancel/i }))
  )
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_CONNECTIONS,
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

  render(<Connections />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
