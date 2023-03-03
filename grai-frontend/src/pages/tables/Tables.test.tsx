import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Tables, { GET_TABLES } from "./Tables"

test("renders", async () => {
  render(<Tables />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Tables/i })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Tables />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Tables />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Search"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Search")
  })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Tables />, {
    withRouter: true,
  })

  await act(async () => await user.click(screen.getByTestId("tables-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Tables />, {
    routes: ["/:tableId"],
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    async () => await user.click(container.querySelectorAll("tbody > tr")[0])
  )

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("no tables", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_TABLES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            tables: [],
          },
        },
      },
    },
  ]

  render(<Tables />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeInTheDocument()
  })
})
