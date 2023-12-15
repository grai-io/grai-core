import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { DELETE_CONNECTION } from "components/connections/ConnectionDelete"
import Connections, { GET_CONNECTIONS } from "./Connections"

test("renders", async () => {
  render(<Connections />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Connections/i })

  await screen.findAllByText("Connection 1")
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Connections />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Connections/i })

  await act(async () => await user.click(screen.getByTestId("table-refresh")))

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
        connections: {
          data: [
            {
              id: "1",
              namespace: "default",
              name: "Connection 1",
              is_active: true,
              validated: true,
              connector: {
                id: "1",
                name: "Connector 1",
                events: true,
              },
              runs: { data: [], meta: { total: 0 } },
              last_run: null,
              last_successful_run: null,
            },
          ],
          meta: {
            total: 1,
          },
        },
      },
    },
  },
}

test("delete", async () => {
  const user = userEvent.setup()

  const mocks = [
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

  await screen.findByRole("heading", { name: /Connections/i })

  await screen.findAllByText("Connection 1")

  await act(async () => {
    await user.click(screen.getByTestId("MoreHorizIcon"))
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )
})

test("cancel delete", async () => {
  const user = userEvent.setup()

  const mocks = [
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

  await screen.findByRole("heading", { name: /Connections/i })

  await screen.findAllByText("Connection 1")

  await act(async () => {
    await user.click(screen.getByTestId("MoreHorizIcon"))
  })

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /cancel/i })),
  )
})

test("error", async () => {
  const mocks = [
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

  await screen.findByText("Error!")
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Connections />, {
    withRouter: true,
  })

  await screen.findAllByText("Hello World")

  await act(async () => await user.type(screen.getByRole("textbox"), "Search"))

  await waitFor(() => expect(screen.getByRole("textbox")).toHaveValue("Search"))

  await screen.findByText("No connections found")
})
