import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import FilterCreate, { GET_WORKSPACE } from "./FilterCreate"

test("renders", async () => {
  render(<FilterCreate />, {
    withRouter: true,
  })

  await screen.findByText("Create Filter")

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<FilterCreate />, { mocks, withRouter: true })

  await screen.findByText("Page not found")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_WORKSPACE,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<FilterCreate />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})
