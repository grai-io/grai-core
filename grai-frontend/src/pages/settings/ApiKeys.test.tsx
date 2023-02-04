import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import ApiKeys, { GET_API_KEYS } from "./ApiKeys"

test("renders", async () => {
  renderWithRouter(<ApiKeys />)

  await waitFor(() => {
    screen.getByText("Settings")
  })

  await waitFor(() => {
    screen.getByRole("heading", { name: /Api Keys/i })
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_API_KEYS,
      variables: {
        organisationName: "",
        workspaceName: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<ApiKeys />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("no workspace", async () => {
  const mock = {
    request: {
      query: GET_API_KEYS,
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
  }

  renderWithMocks(<ApiKeys />, [mock])

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})
