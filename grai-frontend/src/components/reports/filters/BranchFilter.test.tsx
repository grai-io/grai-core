import React from "react"
import { fireEvent, render, screen, waitFor, within } from "testing"
import BranchFilter from "./BranchFilter"

const branches = [
  {
    reference: "branchName",
  },
]

test("renders", async () => {
  render(<BranchFilter branches={branches} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Branch")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.queryByText("branchName")).toBeFalsy()
  })
})

test("renders value", async () => {
  render(<BranchFilter branches={branches} />, {
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
    route: "/org/demo/reports/github/owner/repo?branch=branchName",
  })

  await waitFor(() => {
    expect(screen.getByText("Branch")).toBeInTheDocument()
  })

  const combobox = screen.getByRole("combobox")
  expect(combobox).toHaveProperty("value", "branchName")
})

test("change", async () => {
  render(<BranchFilter branches={branches} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Branch")).toBeInTheDocument()
  })

  const autocomplete = screen.getByTestId("autocomplete")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "br" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })
})
