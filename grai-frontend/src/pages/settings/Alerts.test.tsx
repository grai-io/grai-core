import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Alerts, { GET_ALERTS } from "./Alerts"

test("renders", async () => {
  render(<Alerts />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Alerts/i })).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_ALERTS,
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

  render(<Alerts />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_ALERTS,
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

  render(<Alerts />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})
