import React from "react"
import userEvent from "@testing-library/user-event"
import { UserEvent } from "@testing-library/user-event/dist/types/setup/setup"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import { GET_CONNECTORS } from "./ConnectorSelect"
import CreateConnectionWizard, {
  CREATE_CONNECTION,
} from "./CreateConnectionWizard"

jest.setTimeout(30000)

test("renders", async () => {
  render(<CreateConnectionWizard workspaceId="1" />, {
    withRouter: true,
  })

  expect(screen.getByText("Select a connector")).toBeInTheDocument()
})

test("close", async () => {
  const user = userEvent.setup()

  render(<CreateConnectionWizard workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/connections"],
  })

  expect(screen.getByText("Select a connector")).toBeInTheDocument()

  user.click(screen.getByTestId("CloseIcon"))

  await waitFor(() => {
    expect(screen.queryByText("Select a connector")).toBeFalsy()
  })

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

const connectorsMock = {
  request: {
    query: GET_CONNECTORS,
  },
  result: {
    data: {
      connectors: [
        {
          id: "1",
          name: "PostgreSQL",
          category: "databases",
          coming_soon: false,
          icon: "",
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
        },
      ],
    },
  },
}

const submit = async (user: UserEvent, container: HTMLElement) => {
  expect(screen.getByText("Select a connector")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /PostgreSQL/i })).toBeTruthy()
  })

  await user.click(screen.getByRole("button", { name: /PostgreSQL/i }))

  await waitFor(() => {
    expect(screen.queryByText("Select a connector")).toBeFalsy()
  })

  expect(screen.getByText("Connect to PostgreSQL")).toBeInTheDocument()

  await user.type(screen.getByRole("textbox", { name: "Namespace" }), "default")

  await user.type(
    screen.getByRole("textbox", { name: "Name" }),
    "test connection"
  )
  await user.type(
    screen.getByRole("textbox", { name: "Database Name" }),
    "test"
  )
  await user.type(screen.getByRole("textbox", { name: "user" }), "test")
  await user.type(screen.getByRole("textbox", { name: "host" }), "test")
  await user.type(screen.getByRole("textbox", { name: "port" }), "5432")

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField) await user.type(secretField, "password")

  await user.click(screen.getByRole("button", { name: /continue/i }))

  await waitFor(() => {
    expect(screen.queryByText("Connect to PostgreSQL")).toBeFalsy()
  })

  expect(screen.getByText("Test connection to PostgreSQL")).toBeInTheDocument()

  await user.click(screen.getByRole("button", { name: /continue/i }))

  await waitFor(() => {
    expect(screen.queryByText("Test connection to PostgreSQL")).toBeFalsy()
  })

  expect(
    screen.getByText("Set a schedule for this connection")
  ).toBeInTheDocument()

  await user.click(screen.getByTestId("cron-expression"))

  await user.type(screen.getByRole("textbox", { name: "Minutes" }), "10,30")
  await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8")

  await user.click(screen.getByRole("button", { name: /finish/i }))
}

test("submit", async () => {
  const user = userEvent.setup()

  const createMock = {
    request: {
      query: CREATE_CONNECTION,
      variables: {
        workspaceId: "1",
        connectorId: "1",
        namespace: "defaultdefault",
        name: "PostgreSQLtest connection",
        metadata: { dbname: "test", user: "test", host: "test", port: "5432" },
        secrets: { password: "password" },
        schedules: {
          type: "cron",
          cron: {
            minutes: "10,30",
            hours: "*1,8",
            day_of_week: "*",
            day_of_month: "*",
            month_of_year: "*",
          },
        },
        is_active: true,
      },
    },
    result: {
      data: {
        createConnection: {
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
          is_active: true,
          created_at: "",
          updated_at: "",
        },
      },
    },
  }

  const { container } = render(<CreateConnectionWizard workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/connections/:connectionId"],
    mocks: [connectorsMock, createMock],
  })

  await submit(user, container)

  await waitFor(() => {
    expect(screen.queryByText("Set a schedule for this connection")).toBeFalsy()
  })

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("error", async () => {
  const user = userEvent.setup()

  const createMock = {
    request: {
      query: CREATE_CONNECTION,
      variables: {
        workspaceId: "1",
        connectorId: "1",
        namespace: "defaultdefault",
        name: "PostgreSQLtest connection",
        metadata: { dbname: "test", user: "test", host: "test", port: "5432" },
        secrets: { password: "password" },
        schedules: {
          type: "cron",
          cron: {
            minutes: "10,30",
            hours: "*1,8",
            day_of_week: "*",
            day_of_month: "*",
            month_of_year: "*",
          },
        },
        is_active: true,
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  const { container } = render(<CreateConnectionWizard workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/connections/:connectionId"],
    mocks: [connectorsMock, createMock],
  })

  await submit(user, container)

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
