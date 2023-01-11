import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, renderWithMocks, screen, waitFor } from "testing"
import EditScheduleDialog, { UPDATE_CONNECTION } from "./EditScheduleDialog"

const connection = {
  id: "1",
  schedules: null,
  is_active: false,
  namespace: "default",
  name: "c1",
  metadata: {},
}

test("renders", async () => {
  render(<EditScheduleDialog open onClose={() => {}} connection={connection} />)

  expect(screen.getByText("Edit Schedule")).toBeTruthy()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<EditScheduleDialog open onClose={() => {}} connection={connection} />)

  expect(screen.getByText("Edit Schedule")).toBeTruthy()

  await user.click(screen.getByRole("button", { name: /save/i }))
})

test("submit cron", async () => {
  const user = userEvent.setup()

  render(<EditScheduleDialog open onClose={() => {}} connection={connection} />)

  expect(screen.getByText("Edit Schedule")).toBeTruthy()

  await user.click(screen.getByLabelText("Cron expression"))

  await user.type(screen.getByRole("textbox", { name: /minutes/i }), "30")
  await user.type(screen.getByRole("textbox", { name: /hours/i }), "1")
  await user.type(
    screen.getByRole("textbox", { name: /days of the week/i }),
    "1"
  )
  await user.type(
    screen.getByRole("textbox", { name: /days of the month/i }),
    "2"
  )
  await user.type(
    screen.getByRole("textbox", { name: /months of the year/i }),
    "3"
  )
  await user.click(screen.getByLabelText("Enabled"))

  await user.click(screen.getByRole("button", { name: /save/i }))
})

test("error", async () => {
  const user = userEvent.setup()

  const mock = {
    request: {
      query: UPDATE_CONNECTION,
      variables: {
        id: "1",
        schedules: null,
        is_active: false,
        namespace: "default",
        name: "c1",
        metadata: {},
        secrets: {},
      },
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(
    <EditScheduleDialog open onClose={() => {}} connection={connection} />,
    [mock]
  )

  expect(screen.getByText("Edit Schedule")).toBeTruthy()

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
