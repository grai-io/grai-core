import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, fireEvent, waitFor, act } from "testing"
import { UPLOAD_CONNECTOR_FILE } from "./ConnectionFile"
import SetupConnection, { UPDATE_CONNECTION } from "./SetupConnection"

const opts = {
  activeStep: 0,
  setActiveStep: function (activeStep: number): void {
    throw new Error("Function not implemented.")
  },
  forwardStep: function (): void {
    throw new Error("Function not implemented.")
  },
  backStep: function (): void {
    throw new Error("Function not implemented.")
  },
}

test("renders", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test Connector")).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test Connector")).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i }))
  )
})

test("submit update", async () => {
  const user = userEvent.setup()

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      connection={{
        id: "1",
        namespace: "default",
        name: "connection 1",
        metadata: {},
        secrets: {},
      }}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test Connector")).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i }))
  )
})

test("submit update error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_CONNECTION,
        variables: {
          id: "1",
          namespace: "default",
          name: "connection 1",
          metadata: {},
          secrets: {},
          connectionId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      connection={{
        id: "1",
        namespace: "default",
        name: "connection 1",
        metadata: {},
        secrets: {},
      }}
      setConnection={() => {}}
    />,
    {
      mocks,
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test Connector")).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("renders file", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{
        id: "1",
        name: "Test File Connector",
        metadata: {
          file: {
            name: "manifest.json",
            extension: "json",
          },
        },
      }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test File Connector")).toBeInTheDocument()
})

test("renders file yaml", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{
        id: "1",
        name: "Test YAML Connector",
        metadata: {
          file: {
            name: "yaml",
            extension: "yaml",
          },
        },
      }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test YAML Connector")).toBeInTheDocument()
})

test("upload file", async () => {
  const user = userEvent.setup()

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{
        id: "1",
        name: "Test File Connector",
        metadata: {
          file: {
            name: "manifest.json",
            extension: "json",
          },
        },
      }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      routes: ["/:organisationName/:workspaceName/runs/:runId"],
    }
  )

  expect(screen.getByText("Connect to Test File Connector")).toBeInTheDocument()

  window.URL.createObjectURL = jest.fn().mockImplementation(() => "url")

  const inputEl = screen.getByTestId("drop-input")
  const file = new File(["file"], "ping.json", {
    type: "application/json",
  })
  Object.defineProperty(inputEl, "files", {
    value: [file],
  })
  fireEvent.drop(inputEl)
  expect(await screen.findByText("ping.json")).toBeInTheDocument()

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /namespace/i }),
        "test"
      )
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i }))
  )

  await waitFor(() => expect(screen.getByText("New Page")))
})

test("upload wrong file", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{
        id: "1",
        name: "Test File Connector",
        metadata: {
          file: {
            name: "manifest.json",
            extension: "json",
          },
        },
      }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test File Connector")).toBeInTheDocument()

  window.URL.createObjectURL = jest.fn().mockImplementation(() => "url")

  const inputEl = screen.getByTestId("drop-input")
  const file = new File(["file"], "ping.csv", {
    type: "application/csv",
  })
  Object.defineProperty(inputEl, "files", {
    value: [file],
  })
  fireEvent.drop(inputEl)
  expect(
    await screen.findByText("File type must be application/json,.json")
  ).toBeInTheDocument()
})

test("upload file error", async () => {
  const user = userEvent.setup()

  window.URL.createObjectURL = jest.fn().mockImplementation(() => "url")

  const file = new File(["file"], "ping.json", {
    type: "application/json",
  })

  const mocks = [
    {
      request: {
        query: UPLOAD_CONNECTOR_FILE,
        variables: {
          workspaceId: "1",
          connectorId: "1",
          file,
          namespace: "defaulttest",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{
        id: "1",
        name: "Test File Connector",
        metadata: {
          file: {
            name: "manifest.json",
            extension: "json",
          },
        },
      }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      mocks,
      withRouter: true,
    }
  )

  expect(screen.getByText("Connect to Test File Connector")).toBeInTheDocument()

  const inputEl = screen.getByTestId("drop-input")
  Object.defineProperty(inputEl, "files", {
    value: [file],
  })
  fireEvent.drop(inputEl)
  expect(await screen.findByText("ping.json")).toBeInTheDocument()

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /namespace/i }),
        "test"
      )
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("renders coming soon", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={{
        id: "1",
        name: "Test",
        metadata: {},
        coming_soon: true,
      }}
      connection={null}
      setConnection={() => {}}
    />,
    {
      withRouter: true,
    }
  )

  expect(screen.getByText("Test Integration")).toBeInTheDocument()
  expect(screen.getByText("Test coming soon")).toBeInTheDocument()
})
