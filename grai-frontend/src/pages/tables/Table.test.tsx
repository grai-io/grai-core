import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import Table, { GET_TABLE } from "./Table"

test("renders", async () => {
  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLE,
        variables: {
          organisationName: "",
          workspaceName: "",
          tableId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Table />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLE,
        variables: {
          organisationName: "",
          workspaceName: "",
          tableId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            table: null,
            tables: [],
            other_edges: [],
          },
        },
      },
    },
  ]

  render(<Table />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("lineage", async () => {
  const user = userEvent.setup()

  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Lineage")).toBeTruthy()
  })

  await user.click(screen.getByRole("tab", { name: /Lineage/i }))
})
