import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Tables, { GET_TABLES } from "./Tables"

test("renders", async () => {
  renderWithRouter(<Tables />)

  await waitFor(() => {
    screen.getByRole("heading", { name: /Tables/i })
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
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
  }

  renderWithMocks(<Tables />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  renderWithRouter(<Tables />)

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })

  await user.type(screen.getByRole("textbox"), "Search")

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Search")
  })

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  renderWithRouter(<Tables />)

  await user.click(screen.getByTestId("tables-refresh"))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = renderWithRouter(<Tables />, {
    routes: ["/:tableId"],
  })

  await waitFor(() => {
    screen.getAllByText("Hello World")
  })

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeTruthy()
})

test("no tables", async () => {
  const mock = {
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
  }

  renderWithMocks(<Tables />, [mock])

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeTruthy()
  })
})
