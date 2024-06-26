import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import UpdateConnectionTab, { GET_CONNECTION } from "./UpdateConnectionTab"

test("errors", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          workspaceId: "1",
          connectionId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<UpdateConnectionTab workspaceId="1" connectionId="1" />, { mocks })

  await screen.findByText("Error!")
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          workspaceId: "1",
          connectionId: "1",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            connection: null,
          },
        },
      },
    },
  ]

  render(<UpdateConnectionTab workspaceId="1" connectionId="1" />, { mocks })

  await screen.findByText("Page not found")
})
