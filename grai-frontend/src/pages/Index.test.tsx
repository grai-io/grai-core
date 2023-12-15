import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import Index, { GET_WORKSPACES } from "./Index"

test("renders", async () => {
  render(<Index />, {
    routes: ["/:organisationName/:workspaceName"],
  })

  await screen.findByText("New Page")
})

test("no workspaces", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        data: {
          workspaces: [],
        },
      },
    },
  ]

  render(<Index />, { routes: ["/workspaces"], mocks })

  await screen.findByText("New Page")
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

  render(<Index />, { mocks })

  await screen.findByText("Error!")
})
