import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import { CREATE_WORKSPACE } from "components/workspaces/WorkspaceForm"
import WorkspaceCreate from "./WorkspaceCreate"

test("renders", async () => {
  render(<WorkspaceCreate />, {
    route: "/workspaces/create?organisationId=1",
    path: "/workspaces/create",
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Create a workspace/i })
})

test("renders no organisation", async () => {
  render(<WorkspaceCreate />, {
    withRouter: true,
  })

  await screen.findByRole("heading", { name: /Create a workspace/i })

  expect(screen.getByText("No organisationId found")).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<WorkspaceCreate />, {
    route: "/workspaces/create?organisationId=1",
    path: "/workspaces/create",
    withRouter: true,
    routes: ["/Hello World/Hello World"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestWorkspace",
      ),
  )

  await act(async () => await user.click(screen.getByRole("checkbox")))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i })),
  )

  await screen.findByText("New Page")
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_WORKSPACE,
        variables: {
          name: "TestWorkspace",
          organisationId: "1",
          sample_data: false,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceCreate />, {
    route: "/workspaces/create?organisationId=1",
    path: "/workspaces/create",
    withRouter: true,
    mocks,
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestWorkspace",
      ),
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i })),
  )

  await screen.findByText("Error!")
})
