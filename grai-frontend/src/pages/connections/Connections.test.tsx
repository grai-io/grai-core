import React from "react"
import { GraphQLError } from "graphql"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import Connections, { GET_CONNECTIONS } from "./Connections"
import userEvent from "@testing-library/user-event"

test("renders", async () => {
  renderWithRouter(<Connections />)

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  renderWithRouter(<Connections />)

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await user.click(screen.getByTestId("connection-refresh"))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_CONNECTIONS,
      variables: {
        organisationName: "",
        workspaceName: "",
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<Connections />, [mock])

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeTruthy()
  })
})
