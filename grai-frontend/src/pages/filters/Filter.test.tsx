import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
// import { DELETE_FILTER } from "components/filters/FilterDelete"
import Filter, { GET_FILTER } from "./Filter"

test("renders", async () => {
  render(<Filter />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_FILTER,
        variables: {
          organisationName: "",
          workspaceName: "",
          filterId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Filter />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_FILTER,
        variables: {
          organisationName: "",
          workspaceName: "",
          filterId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            filter: null,
            tags: { data: ["tag1"] },
          },
        },
      },
    },
  ]

  render(<Filter />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
