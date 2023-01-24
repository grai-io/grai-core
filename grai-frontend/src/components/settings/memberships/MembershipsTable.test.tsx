import React from "react"
import { renderWithRouter, screen } from "testing"
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
  renderWithRouter(<MembershipsTable memberships={memberships} />)

  expect(screen.getByText("test@user.com")).toBeTruthy()
})

test("empty", async () => {
  renderWithRouter(<MembershipsTable memberships={[]} />)

  expect(screen.getByText("No memberships found")).toBeTruthy()
})

test("loading", async () => {
  renderWithRouter(<MembershipsTable memberships={[]} loading />)

  expect(screen.getByRole("progressbar")).toBeTruthy()
})
