import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { GET_SOURCE_TABLES } from "components/sources/SourceNodes"
import { UPDATE_SOURCE } from "components/sources/UpdateSource"
import Source, { GET_SOURCE } from "./Source"

jest.retryTimes(1)

test("renders", async () => {
  render(<Source />, {
    withRouter: true,
  })

  await screen.findAllByText("Hello World")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_SOURCE,
        variables: {
          organisationName: "",
          workspaceName: "",
          sourceId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Source />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_SOURCE,
        variables: {
          organisationName: "",
          workspaceName: "",
          sourceId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            source: null,
          },
        },
      },
    },
  ]

  render(<Source />, { mocks, withRouter: true })

  await screen.findAllByText("Page not found")
})

const sourceMock = {
  request: {
    query: GET_SOURCE,
    variables: {
      organisationName: "",
      workspaceName: "",
      sourceId: "",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        source: {
          id: "1",
          name: "Source 1",
          priority: 0,
          connections: {
            data: [],
          },
          runs: {
            meta: {
              total: 0,
            },
          },
        },
      },
    },
  },
}

test("submit", async () => {
  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
  })

  await screen.findAllByText("Hello World")

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "test-source",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )
})

test("submit error", async () => {
  const user = userEvent.setup()

  render(<Source />, {
    mocks: [
      sourceMock,
      {
        request: {
          query: UPDATE_SOURCE,
          variables: {
            sourceId: "1",
            name: "Source 1test-source",
            priority: 0,
          },
        },
        result: {
          errors: [new GraphQLError("Error!")],
        },
      },
    ],
    withRouter: true,
  })

  await screen.findByText("Source 1")

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "test-source",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await screen.findByText("Error!")
})

test("renders nodes", async () => {
  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
  })

  await screen.findAllByText("Hello World")

  await screen.findByRole("tab", { name: /nodes/i })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /nodes/i })),
  )

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

const searchMock = (search: string | null = null) => ({
  request: {
    query: GET_SOURCE_TABLES,
    variables: {
      workspaceId: "1",
      sourceId: "1",
      search,
      offset: 0,
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        source: {
          id: "1",
          nodes: {
            data: [],
            meta: {
              filtered: 0,
            },
          },
        },
      },
    },
  },
})

test("empty nodes", async () => {
  const mocks = [sourceMock, searchMock()]

  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
    mocks,
  })

  await screen.findByText("Source 1")

  await screen.findByRole("tab", { name: /nodes/i })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /nodes/i })),
  )

  await screen.findByText("No nodes found")
})

test("search nodes", async () => {
  const mocks = [sourceMock, searchMock(), searchMock("S"), searchMock("Se")]

  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
    mocks,
  })

  await screen.findByText("Source 1")

  await screen.findByRole("tab", { name: /nodes/i })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /nodes/i })),
  )

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})

  await act(async () => await user.type(screen.getByRole("textbox"), "Se"))

  await screen.findByText("No nodes found")
})

test("nodes error", async () => {
  const user = userEvent.setup()

  const mocks = [
    sourceMock,
    {
      request: {
        query: GET_SOURCE_TABLES,
        variables: {
          workspaceId: "1",
          sourceId: "1",
          search: null,
          offset: 0,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Source />, {
    withRouter: true,
    mocks,
  })

  await screen.findByRole("tab", { name: /nodes/i })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /nodes/i })),
  )

  await screen.findByText("Error!")
})

test("nodes click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Source />, {
    routes: ["/:organisationName/:workspaceName/nodes/:nodeId"],
  })

  await screen.findByRole("tab", { name: /nodes/i })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /nodes/i })),
  )

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0]),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("connections click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Source />, {
    routes: ["/:organisationName/:workspaceName/connections/:connectionId"],
  })

  await screen.findAllByText("Hello World")

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0]),
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
