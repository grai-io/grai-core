import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { screen, fireEvent, waitFor, act, render } from "testing"
import { UPLOAD_CONNECTOR_FILE } from "./ConnectionFile"
import SetupConnection, { CREATE_RUN } from "./SetupConnection"
import { CREATE_CONNECTION, UPDATE_CONNECTION } from "./SetupConnectionForm"

const setConnection = jest.fn()

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

const connector = {
  id: "1",
  name: "Test Connector",
  metadata: null,
  icon: "icon",
}

test("renders", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={connector}
      connection={null}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={connector}
      connection={null}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  expect(setConnection).toHaveBeenCalled()
})

test("submit run error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_CONNECTION,
        variables: {
          sourceName: "Test Connector",
          name: "Test Connector",
          namespace: "default",
          metadata: {},
          secrets: {},
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
              name: "Test Connector",
              icon: null,
            },
            source: {
              id: "1",
              name: "Test Connector",
            },
            last_run: null,
            name: "Test Connector",
            namespace: "default",
            metadata: {},
            is_active: true,
            created_at: "12324",
            updated_at: "1234",
          },
        },
      },
    },
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

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={connector}
      connection={null}
      setConnection={setConnection}
    />,
    {
      mocks,
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("submit update", async () => {
  const user = userEvent.setup()

  render(
    <SetupConnection
      workspaceId="1"
      opts={opts}
      connector={connector}
      connection={{
        id: "1",
        namespace: "default",
        name: "connection 1",
        metadata: {},
        secrets: {},
        sourceName: "default",
      }}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /source/i }),
        "test-source",
      ),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
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
          sourceName: "test",
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
      connector={connector}
      connection={{
        id: "1",
        namespace: "default",
        name: "connection 1",
        sourceName: "test",
        metadata: {},
        secrets: {},
      }}
      setConnection={setConnection}
    />,
    {
      mocks,
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /continue/i })),
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
        icon: null,
      }}
      connection={null}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()
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
        icon: null,
      }}
      connection={null}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()
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
        icon: null,
      }}
      connection={null}
      setConnection={setConnection}
    />,
    {
      routes: ["/:organisationName/:workspaceName/runs/:runId"],
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

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
        "test",
      ),
  )

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /source/i }),
        "test-source",
      ),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i })),
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
        icon: null,
      }}
      connection={null}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

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
    await screen.findByText("File type must be application/json,.json"),
  ).toBeInTheDocument()
})

test("upload file error", async () => {
  const user = userEvent.setup()

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
          sourceName: "Test File Connector",
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
        icon: null,
      }}
      connection={null}
      setConnection={setConnection}
    />,
    { withRouter: true, mocks },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

  window.URL.createObjectURL = jest.fn().mockImplementation(() => "url")

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
        "test",
      ),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i })),
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
        status: "coming_soon",
        icon: null,
      }}
      connection={null}
      setConnection={setConnection}
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText("Test coming soon")).toBeInTheDocument()
})
