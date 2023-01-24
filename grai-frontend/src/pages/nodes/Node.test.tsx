import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Node, { GET_NODE } from "./Node"

test("renders", async () => {
  renderWithRouter(<Node />)

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_NODE,
      variables: {
        organisationName: "organisation",
        workspaceName: "workspace",
        nodeId: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Node />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("not found", async () => {
  const mock = {
    request: {
      query: GET_NODE,
      variables: {
        organisationName: "organisation",
        workspaceName: "workspace",
        nodeId: "",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          node: null,
          nodes: [],
          edges: [],
        },
      },
    },
  }

  renderWithMocks(<Node />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("lineage", async () => {
  const user = userEvent.setup()

  renderWithRouter(<Node />)

  await waitFor(() => {
    expect(screen.getAllByText("Lineage")).toBeTruthy()
  })

  await user.click(screen.getByRole("tab", { name: /Lineage/i }))
})
