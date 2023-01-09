import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Memberships, { GET_MEMBERSHIPS } from "./Memberships"

test("renders", async () => {
  renderWithRouter(<Memberships />)

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_MEMBERSHIPS,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Memberships />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("empty", async () => {
  const mock = {
    request: {
      query: GET_MEMBERSHIPS,
      variables: {
        workspaceId: "",
      },
    },
    result: {
      data: {
        workspace: {
          id: "1",
          memberships: [],
        },
      },
    },
  }

  renderWithMocks(<Memberships />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("No memberships found")).toBeTruthy()
  })
})
