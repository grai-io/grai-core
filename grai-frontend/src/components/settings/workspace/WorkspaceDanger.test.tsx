import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { CLEAR_WORKSPACE } from "./ClearWorkspace"
import WorkspaceDanger from "./WorkspaceDanger"

const workspace = {
  id: "1",
  name: "Test Workspace",
}

test("renders", async () => {
  render(<WorkspaceDanger workspace={workspace} />)
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<WorkspaceDanger workspace={workspace} />)

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /Clear Workspace/i }),
      ),
  )

  await waitFor(() => {
    expect(
      screen.getByText(
        "Are you sure you wish to clear the Test Workspace workspace?",
      ),
    ).toBeTruthy()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Clear/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Workspace cleared")).toBeTruthy()
  })
})

test("submit error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CLEAR_WORKSPACE,
        variables: {
          id: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<WorkspaceDanger workspace={workspace} />, { mocks })

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /Clear Workspace/i }),
      ),
  )

  await waitFor(() => {
    expect(
      screen.getByText(
        "Are you sure you wish to clear the Test Workspace workspace?",
      ),
    ).toBeTruthy()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Clear/i })),
  )

  await waitFor(() => {
    expect(
      screen.getByText("Failed to clear workspace ApolloError: Error!"),
    ).toBeInTheDocument()
  })
})
