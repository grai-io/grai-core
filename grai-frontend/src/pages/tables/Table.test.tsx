import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Table, { GET_TABLE } from "./Table"

test("renders", async () => {
  renderWithRouter(<Table />)

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
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
  }

  renderWithMocks(<Table />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("not found", async () => {
  const mock = {
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
  }

  renderWithMocks(<Table />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("lineage", async () => {
  const user = userEvent.setup()

  renderWithRouter(<Table />)

  await waitFor(() => {
    expect(screen.getAllByText("Lineage")).toBeTruthy()
  })

  await user.click(screen.getByRole("tab", { name: /Lineage/i }))
})
