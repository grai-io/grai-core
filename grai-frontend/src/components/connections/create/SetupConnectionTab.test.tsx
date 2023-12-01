import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import SetupConnectionTab, { GET_CONNECTOR } from "./SetupConnectionTab"

test("errors", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTOR,
        variables: {
          connectorId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<SetupConnectionTab workspaceId="1" connectorId="1" />, { mocks })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTOR,
        variables: {
          connectorId: "1",
        },
      },
      result: {
        data: {
          connector: null,
        },
      },
    },
  ]

  render(<SetupConnectionTab workspaceId="1" connectorId="1" />, { mocks })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
