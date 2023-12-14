import userEvent, { UserEvent } from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { CREATE_CONNECTION } from "./SetupConnectionForm"
import SetupConnectionPanel, { CREATE_RUN } from "./SetupConnectionPanel"
import { GET_RUN } from "./ValidateConnection"

const connector = {
  id: "1",
  name: "test connector",
  icon: null,
  metadata: {
    fields: [
      {
        name: "dbname",
        label: "Database Name",
        required: true,
      },
      {
        name: "user",
        required: true,
      },
      {
        name: "password",
        secret: true,
        required: true,
      },
      {
        name: "host",
        required: true,
      },
      {
        name: "port",
        default: 5432,
        required: true,
      },
    ],
  },
}

const submit = async (user: UserEvent, container: HTMLElement) => {
  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Namespace" }),
        "default",
      ),
  )

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test connection",
      ),
  )
  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Database Name" }),
        "test",
      ),
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "user" }), "test"),
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "host" }), "test"),
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "port" }), "5432"),
  )

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField)
    await act(async () => await user.type(secretField, "password"))

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /test connection/i }),
      ),
  )
}

const createConnectionMock = {
  request: {
    query: CREATE_CONNECTION,
    variables: {
      sourceName: "test connector",
      name: "test connectortest connection",
      namespace: "defaultdefault",
      metadata: {
        dbname: "test",
        user: "test",
        host: "test",
        port: "5432",
      },
      secrets: { password: "password" },
      workspaceId: "1",
      connectorId: "1",
    },
  },
  result: {
    data: {
      createConnection: {
        id: "1",
        connector: {
          id: "1",
          name: "test",
          icon: null,
        },
        source: {
          id: "1",
          name: "test connector",
        },
        last_run: null,
        namespace: "defaultdefault",
        name: "test connectortest connection",
        metadata: {
          dbname: "test",
          user: "test",
          host: "test",
          port: "5432",
        },
        is_active: true,
        created_at: "2021-08-04T14:52:00.000Z",
        updated_at: "2021-08-04T14:52:00.000Z",
      },
    },
  },
}

const createRunMock = {
  request: {
    query: CREATE_RUN,
    variables: {
      connectionId: "1",
    },
  },
  result: {
    data: {
      runConnection: {
        id: "1",
      },
    },
  },
}

test("submit", async () => {
  const user = userEvent.setup()

  const mocks = [
    createConnectionMock,
    createRunMock,
    {
      request: {
        query: GET_RUN,
        variables: {
          workspaceId: "1",
          runId: "1",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: {
              id: "1",
              status: "success",
              metadata: {},
              connection: {
                id: "1",
                validated: true,
              },
            },
          },
        },
      },
    },
  ]

  const { container } = render(
    <SetupConnectionPanel
      workspaceId="1"
      connector={connector}
      defaultConnection={null}
    />,
    {
      mocks,
      withRouter: true,
      routes: ["/:organisationName/:workspaceName/connections/create"],
    },
  )

  expect(screen.getByText("Connect to test connector")).toBeInTheDocument()

  await submit(user, container)

  await screen.findByText("Running tests")

  await screen.findByText("All tests successfully passed!")

  await screen.findByText("New Page", {
      timeout: 1500,
    })
})

test("submit validation fails", async () => {
  const user = userEvent.setup()

  const mocks = [
    createConnectionMock,
    createRunMock,
    {
      request: {
        query: GET_RUN,
        variables: {
          workspaceId: "1",
          runId: "1",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: {
              id: "1",
              status: "error",
              metadata: {
                error: "Test Error",
              },
              connection: {
                id: "1",
                validated: true,
              },
            },
          },
        },
      },
    },
  ]

  const { container } = render(
    <SetupConnectionPanel
      workspaceId="1"
      connector={connector}
      defaultConnection={null}
    />,
    {
      mocks,
      withRouter: true,
    },
  )

  expect(screen.getByText("Connect to test connector")).toBeInTheDocument()

  await submit(user, container)

  await screen.findByText("Running tests")

  await screen.findByText("Validation Failed - Test Error")
})

test("errors", async () => {
  const user = userEvent.setup()

  const mocks = [
    createConnectionMock,
    {
      request: {
        query: CREATE_RUN,
        variables: {
          connectionId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  const { container } = render(
    <SetupConnectionPanel
      workspaceId="1"
      connector={connector}
      defaultConnection={null}
    />,
    {
      mocks,
      withRouter: true,
      routes: ["/:organisationName/:workspaceName/connections/create"],
    },
  )

  expect(screen.getByText("Connect to test connector")).toBeInTheDocument()

  await submit(user, container)

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
