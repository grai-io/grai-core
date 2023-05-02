import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import { GET_REPOSITORIES } from "components/settings/installations/GitHubInstallation"
import Installations from "./Installations"

test("renders", async () => {
  render(<Installations />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Installations/i })
    ).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByTestId("GitHubIcon")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
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

  render(<Installations />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPOSITORIES,
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

  render(<Installations />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})
