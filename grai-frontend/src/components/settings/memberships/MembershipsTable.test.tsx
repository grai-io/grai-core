import React from "react"
import { render, screen } from "testing"
import MembershipsTable from "./MembershipsTable"

const memberships = [
  {
    id: "1",
    role: "admin",
    user: {
      id: "1",
      username: "test@user.com",
      first_name: "test",
      last_name: "user",
    },
    is_active: true,
    created_at: "1",
  },
  {
    id: "2",
    role: "admin",
    user: {
      id: "2",
      username: "test2@user.com",
      first_name: "test2",
      last_name: "user",
    },
    is_active: false,
    created_at: "1",
  },
]

test("renders", async () => {
  render(<MembershipsTable memberships={memberships} />, {
    withRouter: true,
  })

  expect(screen.getByText("test@user.com")).toBeInTheDocument()
})

test("empty", async () => {
  render(<MembershipsTable memberships={[]} />, {
    withRouter: true,
  })

  expect(screen.getByText("No memberships found")).toBeInTheDocument()
})

test("loading", async () => {
  render(<MembershipsTable memberships={[]} loading />, {
    withRouter: true,
  })

  expect(screen.getByRole("progressbar")).toBeTruthy()
})
