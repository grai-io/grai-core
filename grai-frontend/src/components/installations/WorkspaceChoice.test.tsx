import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import WorkspaceChoice, { ADD_INSTALLATION } from "./WorkspaceChoice"

const workspaces = [
  {
    id: "1",
    name: "Workspace1",
    organisation: {
      id: "o1",
      name: "Organisation1",
    },
  },
  {
    id: "2",
    name: "Workspace2",
    organisation: {
      id: "o1",
      name: "Organisation1",
    },
  },
  {
    id: "3",
    name: "Workspace3",
    organisation: {
      id: "o2",
      name: "Organisation2",
    },
  },
]

test("renders", async () => {
  const user = userEvent.setup()

  render(<WorkspaceChoice workspaces={workspaces} installationId={1234} />, {
    path: "/post-install",
    route: "/post-install?installation_id=1234",
    routes: ["/Organisation1/Workspace1"],
  })

  await screen.findAllByText("Workspace1")

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Workspace1/i })),
  )

  await screen.findByText("New Page")
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: ADD_INSTALLATION,
        variables: {
          workspaceId: "1",
          installationId: 1234,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceChoice workspaces={workspaces} installationId={1234} />, {
    mocks,
    path: "/post-install",
    route: "/post-install?installation_id=1234",
  })

  await screen.findAllByText("Workspace1")

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Workspace1/i })),
  )

  await screen.findByText("Error!")
})
