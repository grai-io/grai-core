import { GraphQLError } from "graphql"
import React from "react"
import { render, screen, waitFor } from "testing"
import PostInstall from "./PostInstall"

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
