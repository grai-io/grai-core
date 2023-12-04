import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import ConnectionCreate, { GET_WORKSPACE } from "./ConnectionCreate"

test("renders", async () => {
  render(<ConnectionCreate />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Add Source")).toBeInTheDocument()
  })

  expect(
    screen.getByRole("heading", { name: /Select integration/i }),
  ).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
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

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
