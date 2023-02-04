import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen } from "testing"
import RunStatus from "./RunStatus"

const run = {
  id: "1",
  status: "success",
}

test("renders", async () => {
  render(<RunStatus run={run} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeTruthy()
})

test("navigate", async () => {
  const user = userEvent.setup()

  render(<RunStatus run={run} link />, {
    routes: ["/:organisationName/:workspaceName/runs/:runId"],
  })

  expect(screen.getByText("Success")).toBeTruthy()

  await user.click(screen.getByTestId("CheckIcon"))

  expect(screen.getByText("New Page")).toBeTruthy()
})

test("onClick", async () => {
  render(<RunStatus run={run} onClick={() => {}} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeTruthy()
})
