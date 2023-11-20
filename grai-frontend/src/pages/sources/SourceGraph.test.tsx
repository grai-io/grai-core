import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import SourceGraph, { GET_WORKSPACE } from "./SourceGraph"

export const source_graph = [
  {
    id: "1",
    name: "node A",
    icon: "1",
    targets: ["1", "2"],
  },
  {
    id: "2",
    name: "node B",
    icon: null,
    targets: ["2"],
  },
]

test("renders", async () => {
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
          workspace: {
            id: "1",
            name: "Hello World",
            source_graph,
          },
        },
      },
    },
  ]

  render(<SourceGraph />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Hello World/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("node A")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("node B")).toBeTruthy()
  })
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

  render(<SourceGraph />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
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
        },
      },
    },
  ]

  render(<SourceGraph />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
