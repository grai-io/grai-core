import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen } from "testing"
import ReportsTable from "./ReportsTable"

const runs = [
  {
    id: "1",
    status: "success",
    connection: {
      id: "1",
      name: "Connection Name",
      temp: false,
      connector: {
        id: "2",
        name: "Connector 1",
        icon: "/public/bigquery-icon.png",
      },
    },
    created_at: "1234",
    started_at: "1234",
    finished_at: "1243",
    user: {
      id: "1",
      first_name: "FirstName",
      last_name: "LastName",
    },
    commit: {
      reference: "abcd1",
      title: "A Commit",
      branch: {
        reference: "BranchRef",
      },
      pull_request: {
        reference: "123",
        title: "A Pull Request",
      },
      repository: {
        type: "github",
        owner: "owner",
        repo: "repo",
      },
    },
  },
  {
    id: "2",
    status: "failure",
    connection: {
      id: "2",
      name: "Connection Name2",
      temp: true,
      connector: {
        id: "2",
        name: "Connector 1",
        icon: "/public/bigquery-icon.png",
      },
    },
    created_at: "1234",
    started_at: "1234",
    finished_at: "1243",
    user: {
      id: "1",
      first_name: "FirstName",
      last_name: "LastName",
    },
    commit: {
      reference: "abcd1",
      title: "A Commit",
      branch: {
        reference: "BranchRef",
      },
      pull_request: null,
      repository: {
        type: "github",
        owner: "owner",
        repo: "repo",
      },
    },
  },
  {
    id: "3",
    status: "failure",
    connection: {
      id: "2",
      name: "Connection Name2",
      temp: false,
      connector: {
        id: "2",
        name: "Connector 1",
        icon: null,
      },
    },
    created_at: "1234",
    started_at: "1234",
    finished_at: "1243",
    user: null,
    commit: null,
  },
]

test("renders", async () => {
  render(<ReportsTable runs={runs} />, {
    withRouter: true,
  })

  expect(screen.getByText("Connection Name")).toBeTruthy()
})

test("loading", async () => {
  render(<ReportsTable runs={[]} loading />, {
    withRouter: true,
  })

  expect(screen.getByRole("progressbar")).toBeTruthy()
})

test("empty", async () => {
  render(<ReportsTable runs={[]} />, {
    withRouter: true,
  })

  expect(screen.getByText("No reports found")).toBeTruthy()
})

test("row click", async () => {
  const user = userEvent.setup()

  const { container } = render(<ReportsTable runs={runs} />, {
    routes: [
      "/:organisationName/:workspaceName/reports/github/owner/repo/pulls/123",
    ],
  })

  expect(screen.getByText("Success")).toBeInTheDocument()

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[0])

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("row click no pr", async () => {
  const user = userEvent.setup()

  const { container } = render(<ReportsTable runs={runs} />, {
    routes: [
      "/:organisationName/:workspaceName/reports/github/owner/repo/commits/abcd1",
    ],
  })

  expect(screen.getByText("Success")).toBeInTheDocument()

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[1])

  expect(screen.getByText("New Page")).toBeInTheDocument()
})

test("row click no commit", async () => {
  const user = userEvent.setup()

  const { container } = render(<ReportsTable runs={runs} />, {
    routes: ["/:organisationName/:workspaceName/runs/3"],
  })

  expect(screen.getByText("Success")).toBeInTheDocument()

  // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
  await user.click(container.querySelectorAll("tbody > tr")[2])

  expect(screen.getByText("New Page")).toBeInTheDocument()
})
