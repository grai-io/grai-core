import React from "react"
import userEvent from "@testing-library/user-event"
import { UserEvent } from "@testing-library/user-event/dist/types/setup/setup"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { GET_CONNECTORS } from "./ConnectorSelect"
import CreateConnectionWizard from "./CreateConnectionWizard"
import { UPDATE_CONNECTION } from "./SetSchedule"
import { CREATE_CONNECTION } from "./SetupConnection"
import { CREATE_RUN } from "./TestConnection"
import { GET_RUN } from "./ValidationRun"

jest.setTimeout(30000)

test("renders", async () => {
  render(<CreateConnectionWizard workspaceId="1" />, {
    withRouter: true,
  })

  expect(screen.getByText("Select an integration")).toBeInTheDocument()
})

test("close", async () => {
  const user = userEvent.setup()

  render(<CreateConnectionWizard workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/connections"],
  })

  expect(screen.getByText("Select an integration")).toBeInTheDocument()

  user.click(screen.getByTestId("CloseIcon"))

  await waitFor(() => {
    expect(screen.queryByText("Select an integration")).toBeFalsy()
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
  expect(screen.getByText("Select an integration")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /PostgreSQL/i })).toBeTruthy()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /PostgreSQL/i }))
  )

  await waitFor(() => {
    expect(screen.queryByText("Select an integration")).toBeFalsy()
  })

  expect(screen.getByText("Connect to PostgreSQL")).toBeInTheDocument()

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Namespace" }),
        "default"
      )
  )

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test connection"
      )
  )
  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Database Name" }),
        "test"
      )
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "user" }), "test")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "host" }), "test")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "port" }), "5432")
  )

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField)
    await act(async () => await user.type(secretField, "password"))

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i }))
  )
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

  const validateMock = {
    request: {
      query: CREATE_RUN,
      variables: {
        connectionId: "1",
      },
    },
    result: {
      data: {
        runConnection: {
          __typename: "RunType",
          id: "1",
          status: "queued",
        },
      },
    },
  }

  const getRunMock = {
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
          },
        },
      },
    },
  }

  const updateMock = {
    request: {
      query: UPDATE_CONNECTION,
      variables: {
        id: "1",
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
        updateConnection: {
          __typename: "ConnectionType",
          id: "1",
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
    },
  }

  const { container } = render(<CreateConnectionWizard workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/connections/:connectionId"],
    mocks: [connectorsMock, createMock, validateMock, getRunMock, updateMock],
  })

  await submit(user, container)

  await waitFor(() => {
    expect(screen.queryByText("Connect to PostgreSQL")).toBeFalsy()
  })

  expect(screen.getByText("Test connection to PostgreSQL")).toBeInTheDocument()

  const progressbar = screen.queryByRole("progressbar")

  if (progressbar) {
    // eslint-disable-next-line jest/no-conditional-expect
    await waitFor(() => expect(screen.queryByRole("progressbar")).toBeFalsy())
  }

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /continue/i })).toBeEnabled()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i }))
  )

  await waitFor(() => {
    expect(screen.queryByText("Test connection to PostgreSQL")).toBeFalsy()
  })

  expect(
    screen.getByText("Set a schedule for this connection")
  ).toBeInTheDocument()

  await act(async () => await user.click(screen.getByTestId("cron-expression")))

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Minutes" }), "10,30")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8")
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i }))
  )

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
