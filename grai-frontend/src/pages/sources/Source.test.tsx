import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Source, { GET_SOURCE } from "./Source"
import { GET_SOURCE_TABLES } from "components/sources/SourceTables"

test("renders", async () => {
  render(<Source />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
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

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
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
          connections: {
            data: [],
          },
        },
      },
    },
  },
}

test("renders tables", async () => {
  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByRole("tab", { name: /tables/i })).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /tables/i }))
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

test("empty tables", async () => {
  const mocks = [sourceMock, searchMock()]

  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Source 1")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("tab", { name: /tables/i })).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /tables/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})

test("search tables", async () => {
  const mocks = [sourceMock, searchMock(), searchMock("S"), searchMock("Se")]

  const user = userEvent.setup()

  render(<Source />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Source 1")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("tab", { name: /tables/i })).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /tables/i }))
  )

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})

  await act(async () => await user.type(screen.getByRole("textbox"), "Se"))

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})

test("tables error", async () => {
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

  await waitFor(() => {
    expect(screen.getByRole("tab", { name: /tables/i })).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /tables/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("tables click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Source />, {
    routes: ["/:organisationName/:workspaceName/tables/:tableId"],
  })

  await waitFor(() => {
    expect(screen.getByRole("tab", { name: /tables/i })).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /tables/i }))
  )

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0])
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
