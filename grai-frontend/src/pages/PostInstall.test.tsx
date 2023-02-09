import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import PostInstall, { ADD_INSTALLATION } from "./PostInstall"

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
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: ADD_INSTALLATION,
        variables: {
          installationId: 1234,
        },
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
