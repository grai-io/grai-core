import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { screen, fireEvent, waitFor, act, render } from "testing"
import { UPLOAD_CONNECTOR_FILE } from "./ConnectionFile"
import SetupConnection from "./SetupConnection"
import { CREATE_CONNECTION, UPDATE_CONNECTION } from "./SetupConnectionForm"
import { CREATE_RUN } from "./SetupConnectionPanel"

const connector = {
  id: "1",
  name: "Test Connector",
  metadata: null,
  icon: "icon",
}

test("renders", async () => {
  render(
    <SetupConnection workspaceId="1" connector={connector} connection={null} />,
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
    <SetupConnection workspaceId="1" connector={connector} connection={null} />,
    {
      withRouter: true,
    },
  )

  expect(
    screen.getByRole("heading", { name: /Setup connection/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /test connection/i }),
      ),
  )

  //TODO: Add test here
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
    <SetupConnection workspaceId="1" connector={connector} connection={null} />,
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
      await user.click(
        screen.getByRole("button", { name: /test connection/i }),
      ),
  )

  await screen.findByText("Error!")
})

test("submit update", async () => {
  const user = userEvent.setup()

  render(
    <SetupConnection
      workspaceId="1"
      connector={connector}
      connection={{
        id: "1",
        namespace: "default",
        name: "connection 1",
        metadata: {},
        secrets: {},
        sourceName: "default",
      }}
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
      await user.click(
        screen.getByRole("button", { name: /test connection/i }),
      ),
  )
})

test("submit update error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_CONNECTION,
        variables: {
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
      connector={connector}
      connection={{
        id: "1",
        namespace: "default",
        name: "connection 1",
        sourceName: "test",
        metadata: {},
        secrets: {},
      }}
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
      await user.click(
        screen.getByRole("button", { name: /test connection/i }),
      ),
  )

  await screen.findByText("Error!")
})

test("renders file", async () => {
  render(
    <SetupConnection
      workspaceId="1"
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

  await screen.findByText("Error!")
})

test("renders coming soon", async () => {
  render(
    <SetupConnection
      workspaceId="1"
      connector={{
        id: "1",
        name: "Test",
        metadata: {},
        status: "coming_soon",
        icon: null,
      }}
      connection={null}
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText("Test coming soon")).toBeInTheDocument()
})
