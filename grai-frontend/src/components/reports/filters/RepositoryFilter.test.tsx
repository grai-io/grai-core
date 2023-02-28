import React from "react"
import userEvent from "@testing-library/user-event"
import { fireEvent, render, screen, waitFor, within } from "testing"
import RepositoryFilter from "./RepositoryFilter"

const repositories = [
  {
    type: "github",
    owner: "owner",
    repo: "repo",
  },
]

test("renders", async () => {
  render(<RepositoryFilter repositories={repositories} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Repository")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.queryByText("owner/repo")).toBeFalsy()
  })
})

test("renders value", async () => {
  render(<RepositoryFilter repositories={repositories} />, {
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports?repository=owner/repo",
  })

  await waitFor(() => {
    expect(screen.getByText("Repository")).toBeInTheDocument()
  })

  const combobox = screen.getByRole("combobox")
  expect(combobox).toHaveProperty("value", "owner/repo")
})

test("change", async () => {
  render(<RepositoryFilter repositories={repositories} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Repository")).toBeInTheDocument()
  })

  const autocomplete = screen.getByTestId("autocomplete")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "ow" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })
})

test("clear", async () => {
  const user = userEvent.setup()

  render(<RepositoryFilter repositories={repositories} />, {
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports?repository=owner/repo",
  })

  await waitFor(() => {
    expect(screen.getByText("Repository")).toBeInTheDocument()
  })

  const combobox = screen.getByRole("combobox")
  expect(combobox).toHaveProperty("value", "owner/repo")

  const autocomplete = screen.getByTestId("autocomplete")
  autocomplete.focus()
  await user.click(screen.getByTitle("Clear"))
})
