import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Settings, { GET_WORKSPACE } from "./Settings"

test("renders", async () => {
  const user = userEvent.setup()

  render(<Settings />, {
    path: "/:organisationName/:workspaceName/settings",
    route: "/default/demo/settings",
    routes: ["/default/demo/settings/profile"],
  })

  await waitFor(() => {
    expect(screen.getByText("Settings")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByTestId("AccountCircleIcon")).toBeInTheDocument()
  })

  await act(
    async () => await user.click(screen.getByTestId("AccountCircleIcon"))
  )
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

  render(<Settings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
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

  render(<Settings />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
