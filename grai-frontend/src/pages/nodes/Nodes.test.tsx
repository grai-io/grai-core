import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Nodes, { GET_NODES } from "./Nodes"

test("renders", async () => {
  renderWithRouter(<Nodes />)

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
      query: GET_NODES,
      variables: {
        organisationName: "organisation",
        workspaceName: "workspace",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Nodes />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  renderWithRouter(<Nodes />)

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

  renderWithRouter(<Nodes />)

  await user.click(screen.getByTestId("nodes-refresh"))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("no nodes", async () => {
  const mock = {
    request: {
      query: GET_NODES,
      variables: {
        organisationName: "organisation",
        workspaceName: "workspace",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1234",
          nodes: [],
        },
      },
    },
  }

  renderWithMocks(<Nodes />, [mock])

  await waitFor(() => {
    expect(screen.getByText("No tables found")).toBeTruthy()
  })
})
