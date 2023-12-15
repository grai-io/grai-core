import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import FilterSave, { CREATE_FILTER } from "./FilterSave"

test("renders empty", async () => {
  render(<FilterSave workspaceId="1" inlineFilters={[]} />)

  expect(
    screen.getByRole("button", { name: /save filter/i }),
  ).toBeInTheDocument()
})

test("save", async () => {
  const user = userEvent.setup()

  const inlineFilters = [
    {
      type: null,
      field: null,
      operator: null,
      value: null,
    },
  ]

  render(<FilterSave workspaceId="1" inlineFilters={inlineFilters} />)

  expect(
    screen.getByRole("button", { name: /save filter/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /save filter/i })),
  )

  await screen.findByRole("textbox")

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await screen.findByText("Filter created")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: CREATE_FILTER,
        variables: {
          workspaceId: "1",
          metadata: [{ type: null, field: null, operator: null, value: null }],
          name: "test",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  const user = userEvent.setup()

  const inlineFilters = [
    {
      type: null,
      field: null,
      operator: null,
      value: null,
    },
  ]

  render(<FilterSave workspaceId="1" inlineFilters={inlineFilters} />, {
    mocks,
  })

  expect(
    screen.getByRole("button", { name: /save filter/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /save filter/i })),
  )

  await screen.findByRole("textbox")

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i })),
  )

  await screen.findByText("Error!")
})
