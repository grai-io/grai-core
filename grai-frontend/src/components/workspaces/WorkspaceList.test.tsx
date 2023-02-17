import React from "react"
import { render, screen } from "testing"
import WorkspaceList from "./WorkspaceList"

test("renders", async () => {
  const workspaces = [
    {
      id: "1",
      name: "Workspace1",
      organisation: {
        id: "o1",
        name: "Organisation1",
      },
    },
    {
      id: "2",
      name: "Workspace2",
      organisation: {
        id: "o1",
        name: "Organisation1",
      },
    },
    {
      id: "3",
      name: "Workspace3",
      organisation: {
        id: "o2",
        name: "Organisation2",
      },
    },
  ]

  render(<WorkspaceList workspaces={workspaces} />, { withRouter: true })

  expect(screen.getByText("Organisation1")).toBeInTheDocument()
  expect(screen.getByText("Organisation2")).toBeInTheDocument()
  expect(screen.getByText("Workspace1")).toBeInTheDocument()
  expect(screen.getByText("Workspace2")).toBeInTheDocument()
  expect(screen.getByText("Workspace3")).toBeInTheDocument()
})
