import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Memberships, { GET_MEMBERSHIPS } from "./Memberships"

test("renders", async () => {
  render(<Memberships />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_MEMBERSHIPS,
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

  render(<Memberships />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("empty", async () => {
  const mocks = [
    {
      request: {
        query: GET_MEMBERSHIPS,
        variables: {
          organisationName: "",
          workspaceName: "",
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
    },
  ]

  render(<Memberships />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("No memberships found")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_MEMBERSHIPS,
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

  render(<Memberships />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})
