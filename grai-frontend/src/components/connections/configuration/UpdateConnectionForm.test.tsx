import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import UpdateConnectionForm, { UPDATE_CONNECTION } from "./UpdateConnectionForm"

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

test("renders", async () => {
  render(<UpdateConnectionForm connection={connection} />, {
    withRouter: true,
  })
})

test("submit", async () => {
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
    },
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
    },
  ]

  const { container } = render(
    <UpdateConnectionForm connection={connection} />,
    { mocks }
  )

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
        screen.getByRole("textbox", { name: "Field 1" }),
        "value1"
      )
  )

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /edit/i })).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByRole("button", { name: /edit/i }))
  )

  await waitFor(() => {
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    expect(container.querySelector("input[type=password]")).toBeInTheDocument()
  })

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField) await act(async () => await user.type(secretField, "value2"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )
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

  const { container } = render(
    <UpdateConnectionForm connection={connection} />,
    { mocks }
  )

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
        screen.getByRole("textbox", { name: "Field 1" }),
        "value1"
      )
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
