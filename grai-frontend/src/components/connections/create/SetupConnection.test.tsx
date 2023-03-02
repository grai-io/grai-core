import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen, fireEvent, waitFor, act } from "testing"
import SetupConnection from "./SetupConnection"

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
  // const user = userEvent.setup()

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

// test("upload file error", async () => {
//   const user = userEvent.setup()

//   const mock = {
//     request: {
//       query: UPLOAD_CONNECTOR_FILE,
//       variables: {
//         workspaceId: "",
//         connectorId: "1",
//         file: { path: "ping.json" },
//         namespace: "defaulttest",
//       },
//     },
//     result: {
//       errors: [new GraphQLError("Error!")],
//     },
//   }

//   renderWithMocks(
//     <SetupConnection
//       opts={opts}
//       values={{
//         connector: {
//           id: "1",
//           name: "Test File Connector",
//           metadata: {
//             file: {
//               name: "manifest.json",
//               extension: "json",
//             },
//           },
//         },
//         namespace: "",
//         name: "",
//         metadata: undefined,
//         secrets: undefined,
//         schedules: null,
//       }}
//       setValues={function (values: Values): void {
//         throw new Error("Function not implemented.")
//       }}
//     />,
//     [mock]
//   )

//   expect(screen.getByText("Connect to Test File Connector")).toBeInTheDocument()

//   window.URL.createObjectURL = jest.fn().mockImplementation(() => "url")

//   const inputEl = screen.getByTestId("drop-input")
//   const file = new File(["file"], "ping.json", {
//     type: "application/json",
//   })
//   Object.defineProperty(inputEl, "files", {
//     value: [file],
//   })
//   fireEvent.drop(inputEl)
//   expect(await screen.findByText("ping.json")).toBeInTheDocument()

//   await user.type(screen.getByRole("textbox", { name: /namespace/i }), "test")

//   await user.click(screen.getByRole("button", { name: /finish/i }))
// })
