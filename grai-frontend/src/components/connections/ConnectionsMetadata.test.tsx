import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ConnectionsMetadata from "./ConnectionsMetadata"

const defaultProps = {
  connector: {
    id: "1",
    name: "Connector 1",
    metadata: {},
  },
  metadata: {},
  secrets: {},
  onChangeMetadata: (value: any) => {},
  onChangeSecrets: (value: any) => {},
}

test("renders", async () => {
  render(<ConnectionsMetadata {...defaultProps} />)
})

test("renders edit", async () => {
  render(<ConnectionsMetadata {...defaultProps} edit />)
})

test("normal field", async () => {
  const user = userEvent.setup()

  const props = {
    ...defaultProps,
    connector: {
      ...defaultProps.connector,
      metadata: {
        fields: [
          {
            name: "field1",
            label: "Field 1",
            helper_text: "Helper text",
          },
        ],
      },
    },
  }

  render(<ConnectionsMetadata {...props} />)

  await waitFor(() => {
    expect(screen.getAllByText("Field 1")).toBeTruthy()
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /Field 1/i }),
        "field value"
      )
  )
})

test("secret field", async () => {
  const user = userEvent.setup()

  const props = {
    ...defaultProps,
    connector: {
      ...defaultProps.connector,
      metadata: {
        fields: [
          {
            name: "field1",
            label: "Field 1",
            secret: true,
            helper_text: "Helper text",
          },
        ],
      },
    },
  }

  render(<ConnectionsMetadata {...props} />)

  await waitFor(() => {
    expect(screen.getAllByText("Field 1")).toBeTruthy()
  })

  await act(
    async () => await user.type(screen.getByLabelText("Field 1"), "field value")
  )
})

test("no label", async () => {
  const props = {
    ...defaultProps,
    connector: {
      ...defaultProps.connector,
      metadata: {
        fields: [
          {
            name: "field1",
          },
        ],
      },
    },
  }

  render(<ConnectionsMetadata {...props} />)

  await waitFor(() => {
    expect(screen.getAllByText("field1")).toBeTruthy()
  })
})

test("no label secret", async () => {
  const props = {
    ...defaultProps,
    connector: {
      ...defaultProps.connector,
      metadata: {
        fields: [
          {
            name: "field1",
            secret: true,
          },
        ],
      },
    },
  }

  render(<ConnectionsMetadata {...props} />)

  await waitFor(() => {
    expect(screen.getAllByText("field1")).toBeTruthy()
  })
})
