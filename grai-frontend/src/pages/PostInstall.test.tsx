import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import PostInstall, { GET_WORKSPACES } from "./PostInstall"

test("renders", async () => {
  render(<PostInstall />, {
    path: "/post-install",
    route: "/post-install?installation_id=1234",
    routes: ["/"],
  })

  await screen.findByRole("progressbar")

  await screen.findAllByText("Hello World")
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

  await screen.findByText("Error!")
})
