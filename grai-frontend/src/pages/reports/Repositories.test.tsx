import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Repositories, { GET_REPOSITORIES } from "./Repositories"

test("renders", async () => {
  render(<Repositories />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Select Repository/i })
    ).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Repositories />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner",
    route: "/org/demo/reports/github/owner",
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("empty", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
          type: "github",
          owner: "owner",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            repositories: null,
          },
        },
      },
    },
  ]

  render(<Repositories />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports/:type/:owner",
    route: "/org/demo/reports/github/owner",
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Select Repository/i })
    ).toBeTruthy()
  })
})
