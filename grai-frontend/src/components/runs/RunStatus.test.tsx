import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import RunStatus from "./RunStatus"

const run = {
  id: "1",
  status: "success",
}

test("renders", async () => {
  render(<RunStatus run={run} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
})

test("navigate", async () => {
  const user = userEvent.setup()

  render(<RunStatus run={run} link />, {
    routes: ["/:organisationName/:workspaceName/runs/:runId"],
  })

  expect(screen.getByText("Success")).toBeInTheDocument()

  await act(async () => await user.click(screen.getByTestId("CheckIcon")))

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("onClick", async () => {
  render(<RunStatus run={run} onClick={() => {}} />, {
    withRouter: true,
  })

  expect(screen.getByText("Success")).toBeInTheDocument()
})
