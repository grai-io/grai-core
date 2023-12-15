import { GraphQLError } from "graphql"
import { render, screen } from "testing"
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

  await screen.findByRole("heading", { name: /Hello World/i })

  await screen.findByText("node A")

  await screen.findByText("node B")
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

  await screen.findByText("Error!")
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

  await screen.findAllByText("Page not found")
})
