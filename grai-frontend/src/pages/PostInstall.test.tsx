import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import PostInstall, { GET_WORKSPACES } from "./PostInstall"

test("renders", async () => {
  render(<PostInstall />, {
    path: "/post-install",
    route: "/post-install?installation_id=1234",
    routes: ["/"],
  })

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<PostInstall />, {
    mocks,
    path: "/post-install",
    route: "/post-install?installation_id=1234",
    routes: ["/"],
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
