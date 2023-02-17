import React from "react"
import { render, screen } from "testing"
import ReportFilter from "./ReportFilter"

const workspace = {
  repositories: [
    {
      type: "github",
      owner: "owner",
      repo: "repo",
      branches: [
        {
          reference: "branch1",
        },
        {
          reference: "branch2",
        },
      ],
      pull_requests: [
        {
          reference: "pr1",
          title: "pr1title",
        },
        {
          reference: "pr2",
          title: "pr2title",
        },
      ],
    },
    {
      type: "github",
      owner: "owner",
      repo: "repo2",
      branches: [
        {
          reference: "branch3",
        },
        {
          reference: "branch4",
        },
      ],
      pull_requests: [
        {
          reference: "pr3",
          title: "pr3title",
        },
        {
          reference: "pr3",
          title: "pr3title",
        },
      ],
    },
  ],
}

test("renders", async () => {
  render(<ReportFilter workspace={workspace} />, {
    withRouter: true,
  })

  expect(screen.getByText("Repository")).toBeTruthy()
  expect(screen.getByText("Branch")).toBeTruthy()
})

test("renders filtered", async () => {
  render(<ReportFilter workspace={workspace} />, {
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports?repository=owner/repo",
  })

  expect(screen.getByText("Repository")).toBeTruthy()
  expect(screen.getByText("Branch")).toBeTruthy()

  const combobox = screen.getAllByRole("combobox")[0]
  expect(combobox).toHaveProperty("value", "owner/repo")
})
