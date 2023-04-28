import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import UpdateFilter, { UPDATE_FILTER } from "./UpdateFilter"

const filter = {
  id: "1",
  name: "test filter",
  metadata: [],
}

test("renders", async () => {
  render(<UpdateFilter filter={filter} tags={[]} />, {
    withRouter: true,
  })

  expect(screen.getByRole("textbox", { name: /name/i })).toBeInTheDocument()
})

test("renders null name", async () => {
  const filter = {
    id: "1",
    name: null,
    metadata: [],
  }

  render(<UpdateFilter filter={filter} tags={[]} />, {
    withRouter: true,
  })

  expect(screen.getByRole("textbox", { name: /name/i })).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<UpdateFilter filter={filter} tags={[]} />, {
    withRouter: true,
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Name" }),
        "test filter"
      )
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )
})

test("submit error", async () => {
  const user = userEvent.setup()

  render(<UpdateFilter filter={filter} tags={[]} />, {
    withRouter: true,
    mocks: [
      {
        request: {
          query: UPDATE_FILTER,
          variables: {
            id: "1",
            name: "test filtera",
            metadata: [],
          },
        },
        result: {
          errors: [new GraphQLError("Error!")],
        },
      },
    ],
  })

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Name" }), "a")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
