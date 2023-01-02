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
import CreateConnectionForm, { CREATE_CONNECTION } from "./CreateConnectionForm"

test("renders", async () => {
  renderWithRouter(<CreateConnectionForm />)

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).toBeFalsy()
  })
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
        connectorId: "1",
        namespace: "default",
        name: "test connection",
        metadata: {
          field1: "value1",
        },
        secrets: {
          field2: "value2",
        },
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

  const { container } = renderWithMocks(<CreateConnectionForm />, [
    connectorsMock,
    createMock,
  ])

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).toBeFalsy()
  })

  const autocomplete = screen.getByTestId("autocomplete")
  const input = within(autocomplete).getByRole("combobox")
  autocomplete.focus()
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "c" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })

  await user.type(
    screen.getByRole("combobox", { name: /connector/i }),
    "test connection"
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
