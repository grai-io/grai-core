import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Repositories, { GET_REPOSITORIES } from "./Repositories"

test("renders", async () => {
  const mocks = [
    profileMock,
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
            repositories: [
              {
                id: "1",
                type: "github",
                owner: "owner",
                repo: "repo1",
              },
              {
                id: "1",
                type: "github",
                owner: "owner",
                repo: "repo2",
              },
            ],
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

  await waitFor(() => {
    expect(screen.getByText("repo1")).toBeTruthy()
  })
  await waitFor(() => {
    expect(screen.getByText("repo2")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
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
    profileMock,
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
