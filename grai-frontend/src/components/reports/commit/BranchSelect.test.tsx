import React from "react"
import { fireEvent, render, screen, waitFor, within } from "testing"
import BranchSelect from "./BranchSelect"

const branches = [
  {
    reference: "branchName",
  },
]

test("renders", async () => {
  render(<BranchSelect branches={branches} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Branch")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Any")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.queryByText("branchName")).toBeFalsy()
  })
})

test("renders value", async () => {
  render(<BranchSelect branches={branches} />, {
    path: "/:organisationName/:workspaceName/reports/:type/:owner/:repo",
    route: "/org/demo/reports/github/owner/repo?branch=branchName",
  })

  await waitFor(() => {
    expect(screen.getByText("Branch")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.queryByText("Any")).toBeFalsy()
  })

  await waitFor(() => {
    expect(screen.getByText("branchName")).toBeInTheDocument()
  })
})

test("change", async () => {
  render(<BranchSelect branches={branches} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Branch")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("Any")).toBeInTheDocument()
  })

  fireEvent.mouseDown(screen.getByRole("button"))

  const listbox = within(screen.getByRole("listbox"))

  fireEvent.click(listbox.getByText(/branchName/i))

  await waitFor(() => {
    expect(screen.queryByText("Any")).toBeFalsy()
  })

  await waitFor(() => {
    expect(screen.getByText("branchName")).toBeInTheDocument()
  })
})
