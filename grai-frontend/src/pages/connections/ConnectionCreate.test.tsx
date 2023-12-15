import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import ConnectionCreate, { GET_WORKSPACE } from "./ConnectionCreate"

test("renders", async () => {
  render(<ConnectionCreate />, {
    withRouter: true,
  })

  await screen.findByText("Add Source")

  expect(
    screen.getByRole("heading", { name: /Select integration/i }),
  ).toBeInTheDocument()

  await screen.findAllByText("Hello World")
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
          connectors: [],
        },
      },
    },
  ]

  render(<ConnectionCreate />, {
    mocks,
    withRouter: true,
  })

  await screen.findByText("Page not found")
})

test("errors", async () => {
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

  render(<ConnectionCreate />, {
    mocks,
    withRouter: true,
  })

  await screen.findByText("Error!")
})
