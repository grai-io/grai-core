import userEvent from "@testing-library/user-event"
import { GET_CONNECTORS } from "components/form/fields/Connector"
import React from "react"
import { renderWithMocks, renderWithRouter, screen } from "testing"
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
  renderWithRouter(<UpdateConnectionForm connection={connection} />)
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
      query: UPDATE_CONNECTION,
      variables: {
        connectionId: "1",
        namespace: "defaultdefault",
        name: "connection 1test connection",
        metadata: {
          field1: "value1",
        },
        secrets: {},
        // secrets: {
        //   field2: "value2",
        // },
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
          is_active: true,
          created_at: "",
          updated_at: "",
        },
      },
    },
  }

  const { container } = renderWithMocks(
    <UpdateConnectionForm connection={connection} />,
    [connectorsMock, createMock]
  )

  await user.type(screen.getByRole("textbox", { name: "Namespace" }), "default")

  await user.type(
    screen.getByRole("textbox", { name: "Name" }),
    "test connection"
  )

  await user.type(screen.getByRole("textbox", { name: "Field 1" }), "value1")

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  const secretField = container.querySelector("input[type=password]")

  if (secretField) await user.type(secretField, "value2")

  await user.click(screen.getByRole("button", { name: /save/i }))
})
