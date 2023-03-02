import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, waitFor, screen, act } from "testing"
import SetSchedule, { UPDATE_CONNECTION } from "./SetSchedule"

const opts = {
  activeStep: 0,
  setActiveStep: function (activeStep: number): void {
    throw new Error("Function not implemented.")
  },
  forwardStep: function (): void {
    throw new Error("Function not implemented.")
  },
  backStep: function (): void {
    throw new Error("Function not implemented.")
  },
}

const connection = {
  id: "1",
  namespace: "default",
  name: "connection 1",
  metadata: {},
  secrets: {},
}

test("renders", async () => {
  render(
    <SetSchedule opts={opts} connection={connection} onComplete={() => {}} />
  )

  expect(screen.getByText("Set a schedule for this connection")).toBeTruthy()
})

test("submit", async () => {
  const user = userEvent.setup()

  render(
    <SetSchedule opts={opts} connection={connection} onComplete={() => {}} />
  )

  expect(screen.getByText("Set a schedule for this connection")).toBeTruthy()

  await act(async () => await user.click(screen.getByTestId("cron-expression")))

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Minutes" }), "10,30")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8")
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i }))
  )
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

  render(
    <SetSchedule opts={opts} connection={connection} onComplete={() => {}} />,
    { mocks }
  )

  expect(screen.getByText("Set a schedule for this connection")).toBeTruthy()

  await act(async () => await user.click(screen.getByTestId("cron-expression")))

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Minutes" }), "10,30")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: "Hours" }), "1,8")
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
