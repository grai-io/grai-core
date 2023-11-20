import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
// import { DELETE_FILTER } from "components/filters/FilterDelete"
import Filter, { GET_FILTER } from "./Filter"

test("renders", async () => {
  render(<Filter />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
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

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
