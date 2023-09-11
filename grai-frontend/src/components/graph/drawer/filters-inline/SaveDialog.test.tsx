import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import SaveDialog, { CREATE_FILTER } from "./SaveDialog"

const defaultProps = {
  open: true,
  onClose: jest.fn(),
  workspaceId: "1",
  inlineFilters: [],
}

test("renders", async () => {
  render(<SaveDialog {...defaultProps} />)

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument()
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<SaveDialog {...defaultProps} />)

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument()
  })

  await act(async () => user.type(screen.getByLabelText(/name/i), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_FILTER,
        variables: {
          workspaceId: "1",
          name: "test",
          metadata: [],
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<SaveDialog {...defaultProps} />, { mocks })

  await waitFor(() => {
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument()
  })

  await act(async () => user.type(screen.getByLabelText(/name/i), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
