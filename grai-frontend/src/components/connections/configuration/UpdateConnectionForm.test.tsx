import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import UpdateConnectionForm, {
  CREATE_RUN,
  UPDATE_CONNECTION,
} from "./UpdateConnectionForm"
import { GET_RUN } from "../create/ValidateConnection"

const workspace = {
  id: "1",
}

const connection = {
  id: "1",
  namespace: "default",
  name: "connection 1",
  metadata: {},
  connector: {
    id: "1",
    name: "Test Connector 1",
    metadata: {
      fields: [
        {
          name: "field1",
          label: "Field 1",
        },
        {
          name: "field2",
          label: "Field 2",
          secret: true,
        },
      ],
    },
  },
}

const updateMock1 = {
  request: {
    query: UPDATE_CONNECTION,
    variables: {
      connectionId: "1",
      namespace: "defaultdefault",
      name: "connection 1test connection",
      metadata: {
        field1: "value1",
      },
      secrets: {},
      schedules: null,
      is_active: true,
    },
  },
  result: {
    data: {
      updateConnection: {
        __typename: "ConnectionType",
        id: "1",
        connector: {
          id: "1",
          name: "c",
        },
        namespace: "default",
        name: "test connection",
        metadata: {
          field1: "value1",
        },
        secrets: {
          field2: "value2",
        },
        schedules: null,
        is_active: true,
        created_at: "",
        updated_at: "",
      },
    },
  },
}

const updateMock2 = {
  request: {
    query: UPDATE_CONNECTION,
    variables: {
      connectionId: "1",
      namespace: "defaultdefault",
      name: "connection 1test connection",
      metadata: {
        field1: "value1",
      },
      secrets: {
        field2: "value2",
      },
      schedules: null,
      is_active: true,
    },
  },
  result: {
    data: {
      updateConnection: {
        __typename: "ConnectionType",
        id: "1",
        connector: {
          id: "1",
          name: "c",
        },
        namespace: "default",
        name: "test connection",
        metadata: {
          field1: "value1",
        },
        secrets: {
          field2: "value2",
        },
        schedules: null,
        is_active: true,
        created_at: "",
        updated_at: "",
      },
    },
  },
}

test("renders", async () => {
  render(
    <UpdateConnectionForm connection={connection} workspace={workspace} />,
    {
      withRouter: true,
    },
  )
})

test("submit", async () => {
  const user = userEvent.setup()

  const mocks = [
    updateMock1,
    updateMock2,
    {
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
            status: "PENDING",
            created_at: "",
            updated_at: "",
            started_at: "",
            finished_at: "",
            logs: [],
            connection: {
              id: "1",
              name: "test connection",
              namespace: "default",
              connector: {
                id: "1",
                name: "c",
              },
              metadata: {
                field1: "value1",
              },
              secrets: {
                field2: "value2",
              },
              schedules: null,
              is_active: true,
              created_at: "",
              updated_at: "",
            },
          },
        },
      },
    },
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
    <UpdateConnectionForm connection={connection} workspace={workspace} />,
    { mocks },
  )

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
        screen.getByRole("textbox", { name: "Field 1" }),
        "value1",
      ),
  )

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /edit/i })).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /edit/i })),
  )

  await waitFor(() => {
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    expect(container.querySelector("input[type=password]")).toBeInTheDocument()
  })

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField) await act(async () => await user.type(secretField, "value2"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(() => {
    expect(
      screen.getByText("All tests successfully passed!"),
    ).toBeInTheDocument()
  })
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_CONNECTION,
        variables: {
          connectionId: "1",
          namespace: "defaultdefault",
          name: "connection 1test connection",
          metadata: {
            field1: "value1",
          },
          secrets: {},
          schedules: null,
          is_active: true,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <UpdateConnectionForm connection={connection} workspace={workspace} />,
    { mocks },
  )

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
        screen.getByRole("textbox", { name: "Field 1" }),
        "value1",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("submit run error", async () => {
  const user = userEvent.setup()

  const mocks = [
    updateMock1,
    updateMock2,
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
    <UpdateConnectionForm connection={connection} workspace={workspace} />,
    { mocks },
  )

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
        screen.getByRole("textbox", { name: "Field 1" }),
        "value1",
      ),
  )

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /edit/i })).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /edit/i })),
  )

  await waitFor(() => {
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    expect(container.querySelector("input[type=password]")).toBeInTheDocument()
  })

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField) await act(async () => await user.type(secretField, "value2"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(async () => {
    expect(await screen.findByText("Error!")).toBeInTheDocument()
  })
})
