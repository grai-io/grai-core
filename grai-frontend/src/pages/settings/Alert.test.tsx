import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Alert, { GET_ALERT } from "./Alert"

test("renders", async () => {
  render(<Alert />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Hello World/i })
    ).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_ALERT,
        variables: {
          organisationName: "",
          workspaceName: "",
          id: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Alert />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_ALERT,
        variables: {
          organisationName: "",
          workspaceName: "",
          id: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            alert: null,
          },
        },
      },
    },
  ]

  render(<Alert />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})
