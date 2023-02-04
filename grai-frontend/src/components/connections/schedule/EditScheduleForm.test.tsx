import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import EditScheduleForm, { UPDATE_CONNECTION } from "./EditScheduleForm"

const connection = {
  id: "1",
  schedules: null,
  is_active: false,
  namespace: "default",
  name: "c1",
  metadata: {},
}

test("renders", async () => {
  render(<EditScheduleForm connection={connection} />)

  expect(screen.getByText("Schedule type")).toBeInTheDocument()
})

test("renders with schedule", async () => {
  const connection = {
    id: "1",
    schedules: {
      type: "cron",
    },
    is_active: false,
    namespace: "default",
    name: "c1",
    metadata: {},
  }

  render(<EditScheduleForm connection={connection} />)

  expect(screen.getByText("Schedule type")).toBeInTheDocument()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<EditScheduleForm connection={connection} />)

  expect(screen.getByText("Schedule type")).toBeInTheDocument()

  await user.click(screen.getByRole("button", { name: /save/i }))
})

test("submit cron", async () => {
  const user = userEvent.setup()

  render(<EditScheduleForm connection={connection} />)

  expect(screen.getByText("Schedule type")).toBeInTheDocument()

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

  const mocks = [
    {
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
    },
  ]

  render(<EditScheduleForm connection={connection} />, { mocks })

  expect(screen.getByText("Schedule type")).toBeInTheDocument()

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
