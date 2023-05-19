import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ConnectionsMenu from "./ConnectionsMenu"
import ConnectionRunButton from "./ConnectionRunButton"

const connection = {
  id: "1",
  name: "Test Connection",
  runs: { data: [] },
  last_run: null,
  last_successful_run: null,
  connector: {
    events: true,
  },
}

test("renders", async () => {
  render(<ConnectionRunButton onRun={() => {}} status={null} />)
})

test("run", async () => {
  const user = userEvent.setup()

  render(<ConnectionRunButton onRun={() => {}} events status={null} />)

  await act(async () => await user.click(screen.getByText("Run")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("open", async () => {
  const user = userEvent.setup()

  render(<ConnectionRunButton onRun={() => {}} events status={null} />)

  await act(
    async () => await user.click(screen.getByTestId("ArrowDropDownIcon"))
  )

  await waitFor(() => {
    expect(screen.getByText("Run Events")).toBeInTheDocument()
  })

  await user.click(document.body)

  await waitFor(() => {
    expect(screen.queryByText("Run Events")).not.toBeInTheDocument()
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
