import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, waitFor, screen, act } from "testing"
import ScheduleForm, { UPDATE_CONNECTION } from "./ScheduleForm"

const onComplete = jest.fn()

const connection = {
  id: "1",
  namespace: "default",
  name: "connection 1",
  metadata: {},
  secrets: {},
  sourceName: "default",
}

test("renders", async () => {
  render(<ScheduleForm connection={connection} onComplete={onComplete} />)

  expect(screen.getByText(/Schedule type/i)).toBeTruthy()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<ScheduleForm connection={connection} onComplete={onComplete} />)

  expect(screen.getByText(/Schedule type/i)).toBeTruthy()

  await act(async () => await user.click(screen.getByTestId("cron-expression")))

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Minutes" }),
        "10,30",
      ),
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8"),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i })),
  )

  await waitFor(() => expect(onComplete).toHaveBeenCalled())
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_CONNECTION,
        variables: {
          id: "1",
          schedules: {
            type: "cron",
            cron: {
              minutes: "10,30",
              hours: "*1,8",
              day_of_week: "*",
              day_of_month: "*",
              month_of_year: "*",
            },
          },
          is_active: true,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ScheduleForm connection={connection} onComplete={onComplete} />, {
    mocks,
  })

  expect(screen.getByText(/Schedule type/i)).toBeTruthy()

  await act(async () => await user.click(screen.getByTestId("cron-expression")))

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: "Minutes" }),
        "10,30",
      ),
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8"),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i })),
  )

  await screen.findByText("Error!")
})
