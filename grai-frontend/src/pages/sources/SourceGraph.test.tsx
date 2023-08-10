import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import SourceGraph, { GET_WORKSPACE } from "./SourceGraph"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            name: "Hello World",
            source_graph: {
              "node A": ["node A", "node B"],
              "node C": ["node C", "node B"],
            },
          },
        },
      },
    },
  ]

  render(<SourceGraph />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Hello World/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("node A")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("node B")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
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

  render(<SourceGraph />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<SourceGraph />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
