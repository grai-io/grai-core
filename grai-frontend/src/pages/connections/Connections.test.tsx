import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Connections, { GET_CONNECTIONS } from "./Connections"

test("renders", async () => {
  render(<Connections />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Connection 1")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Connections />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Connections/i })).toBeTruthy()
  })

  await user.click(screen.getByTestId("connection-refresh"))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("error", async () => {
  const mocks = [
    {
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
    },
  ]

  render(<Connections />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
