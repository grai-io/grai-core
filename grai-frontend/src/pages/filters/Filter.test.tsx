import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import Filter, { GET_FILTER } from "./Filter"

test("renders", async () => {
  render(<Filter />, {
    withRouter: true,
  })

  await screen.findAllByText("Hello World")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_FILTER,
        variables: {
          organisationName: "",
          workspaceName: "",
          filterId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Filter />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_FILTER,
        variables: {
          organisationName: "",
          workspaceName: "",
          filterId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            filter: null,
            namespaces: { data: ["namespace1"] },
            tags: { data: ["tag1"] },
            sources: [],
          },
        },
      },
    },
  ]

  render(<Filter />, { mocks, withRouter: true })

  await screen.findAllByText("Page not found")
})
