import React from "react"
import { render, screen, waitFor } from "testing"
import FilterCreate, { GET_WORKSPACE } from "./FilterCreate"
import profileMock from "testing/profileMock"
import { GraphQLError } from "graphql"

test("renders", async () => {
  render(<FilterCreate />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Create Filter")).toBeInTheDocument()
  })

  await waitFor(() => {})
})

test("not found", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_WORKSPACE,
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

  render(<FilterCreate />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_WORKSPACE,
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

  render(<FilterCreate />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
