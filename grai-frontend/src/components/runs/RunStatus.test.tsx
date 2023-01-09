import React from "react"
import userEvent from "@testing-library/user-event"
import { renderWithRouter, screen } from "testing"
import RunStatus from "./RunStatus"

const run = {
  id: "1",
  status: "success",
}

test("renders", async () => {
  renderWithRouter(<RunStatus run={run} />)

  expect(screen.getByText("Success")).toBeTruthy()
})

test("navigate", async () => {
  const user = userEvent.setup()

  renderWithRouter(<RunStatus run={run} link />, {
    routes: ["/workspaces/:workspaceId/runs/:runId"],
  })

  expect(screen.getByText("Success")).toBeTruthy()

  await user.click(screen.getByTestId("CheckIcon"))

  expect(screen.getByText("New Page")).toBeTruthy()
})

test("onClick", async () => {
  renderWithRouter(<RunStatus run={run} onClick={() => {}} />)

  expect(screen.getByText("Success")).toBeTruthy()
})
