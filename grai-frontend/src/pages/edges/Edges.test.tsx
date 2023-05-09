import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Edges, { GET_EDGES } from "./Edges"

test("renders", async () => {
  render(<Edges />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Edges/i })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_EDGES,
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

  render(<Edges />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Edges />, {
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
    expect(screen.getByText("No edges found")).toBeInTheDocument()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Edges />, {
    withRouter: true,
  })

  await act(async () => await user.click(screen.getByTestId("table-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("click row", async () => {
  const user = userEvent.setup()

  const { container } = render(<Edges />, {
    routes: ["/:edgeId"],
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

test("no edges", async () => {
  const mocks = [
    {
      request: {
        query: GET_EDGES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1234",
            edges: {
              data: [],
              meta: {
                total: 0,
              },
            },
          },
        },
      },
    },
  ]

  render(<Edges />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("No edges found")).toBeInTheDocument()
  })
})
