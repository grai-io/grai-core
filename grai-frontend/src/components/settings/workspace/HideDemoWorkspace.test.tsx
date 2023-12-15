import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import HideDemoWorkspace, { UPDATE_WORKSPACE } from "./HideDemoWorkspace"

const workspace = {
  id: "1",
}

test("renders", async () => {
  render(<HideDemoWorkspace workspace={workspace} />)
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<HideDemoWorkspace workspace={workspace} />)

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /Hide demo banner/i }))
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_WORKSPACE,
        variables: {
          id: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<HideDemoWorkspace workspace={workspace} />, { mocks })

  await act(async () => {
    await user.click(screen.getByRole("button", { name: /Hide demo banner/i }))
  })

  await screen.findByText("Failed to update workspace ApolloError: Error!")
})
