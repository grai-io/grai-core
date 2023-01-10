import userEvent from "@testing-library/user-event"
import { GET_CONNECTORS } from "components/form/fields/Connector"
import React from "react"
import {
  fireEvent,
  renderWithMocks,
  renderWithRouter,
  screen,
  waitFor,
  within,
} from "testing"
import CreateConnectionWizard, {
  CREATE_CONNECTION,
} from "./CreateConnectionWizard"

test("renders", async () => {
  renderWithRouter(<CreateConnectionWizard />)

  expect(screen.getByText("Select a connector")).toBeTruthy()
})

test("close", async () => {
  const user = userEvent.setup()

  renderWithRouter(<CreateConnectionWizard />, {
    routes: ["/workspaces/:workspaceId/connections"],
  })

  expect(screen.getByText("Select a connector")).toBeTruthy()

  user.click(screen.getByTestId("CloseIcon"))

  await waitFor(() => {
    expect(screen.queryByText("Select a connector")).toBeFalsy()
  })

  expect(screen.getByText("New Page")).toBeTruthy()
})

test("submit", async () => {
  const user = userEvent.setup()

  const connectorsMock = {
    request: {
      query: GET_CONNECTORS,
    },
    result: {
      data: {
        connectors: [
          {
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
        ],
      },
    },
  }

  const createMock = {
    request: {
      query: CREATE_CONNECTION,
      variables: {
        workspaceId: "",
        connectorId: "768aea48-1146-4f14-9005-40e89504f4b3",
        namespace: "default",
        name: "test connectiontest",
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

  const { container } = renderWithMocks(
    <CreateConnectionWizard />,
    [connectorsMock, createMock],
    {
      routes: ["/workspaces/:workspaceId/connections/:connectionId"],
    }
  )

  expect(screen.getByText("Select a connector")).toBeTruthy()

  user.click(screen.getByRole("button", { name: "PostreSQL logo PostreSQL" }))

  await waitFor(() => {
    expect(screen.queryByText("Select a connector")).toBeFalsy()
  })

  expect(screen.getByText("Connect to PostgreSQL")).toBeTruthy()

  await user.type(screen.getByRole("textbox", { name: "Namespace" }), "default")

  await user.type(
    screen.getByRole("textbox", { name: "Name" }),
    "test connection"
  )

  await user.type(screen.getByRole("textbox", { name: "Name" }), "test")
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

  expect(screen.getByText("Test connection to PostgreSQL")).toBeTruthy()

  await user.click(screen.getByRole("button", { name: /continue/i }))

  await waitFor(() => {
    expect(screen.queryByText("Test connection to PostgreSQL")).toBeFalsy()
  })

  expect(screen.getByText("Set a schedule for this connection")).toBeTruthy()

  await user.click(screen.getByTestId("cron-expression"))

  await user.type(screen.getByRole("textbox", { name: "Minutes" }), "10,30")
  await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8")

  await user.click(screen.getByRole("button", { name: /finish/i }))

  await waitFor(() => {
    expect(screen.queryByText("Set a schedule for this connection")).toBeFalsy()
  })

  expect(screen.getByText("New Page")).toBeTruthy()
})
