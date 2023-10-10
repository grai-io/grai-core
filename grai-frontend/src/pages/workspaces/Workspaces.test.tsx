import React from "react"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Workspaces, { GET_WORKSPACES } from "./Workspaces"
import userEvent from "@testing-library/user-event"
import { CREATE_WORKSPACE } from "components/workspaces/OrganisationForm"
import { LOAD_WORKSPACE_SAMPLE_DATA } from "components/workspaces/CreateSampleData"

test("renders", async () => {
  render(<Workspaces />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Select workspace/i }),
    ).toBeInTheDocument()
  })
})

test("no workspaces", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        data: {
          workspaces: [],
        },
      },
    },
    {
      request: {
        query: CREATE_WORKSPACE,
        variables: {
          organisationName: "TestOrganisation",
          name: "production",
          sample_data: false,
        },
      },
      result: {
        data: {
          createWorkspace: {
            id: "1",
            name: "production",
            organisation: {
              id: "1",
              name: "TestOrganisation",
            },
          },
        },
      },
    },
    {
      request: {
        query: LOAD_WORKSPACE_SAMPLE_DATA,
        variables: {
          id: "1",
        },
      },
      result: {
        data: {
          loadWorkspaceSampleData: {
            id: "1",
            name: "production",
            organisation: {
              id: "1",
              name: "TestOrganisation",
            },
          },
        },
      },
    },
  ]

  render(<Workspaces />, { mocks, routes: ["/TestOrganisation/production"] })

  await screen.findByRole("progressbar")
  await waitFor(() => expect(screen.queryByRole("progressbar")).toBeFalsy())

  await waitFor(() =>
    expect(screen.getByRole("heading", { name: /Create an organisation/i })),
  )

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestOrganisation",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i })),
  )

  // await waitFor(() =>
  //   expect(screen.getByText(/Your workspace will be ready very soon/i)),
  // )

  await waitFor(() => expect(screen.getByText(/New Page/i)))
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Workspaces />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  render(<Workspaces />, {
    withRouter: true,
    path: "/workspaces",
    initialEntries: [
      {
        pathname: "/workspaces",
        state: {
          workspaceNotFound: true,
          organisationName: "test",
          workspaceName: "workspace",
        },
      },
    ],
  })

  await waitFor(() => {
    expect(
      screen.getByText("Please contact your administrator"),
    ).toBeInTheDocument()
  })
})
