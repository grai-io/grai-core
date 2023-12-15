import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import HomeCards, { GET_COUNTS } from "./HomeCards"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_COUNTS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            runs: {
              meta: {
                filtered: 38,
              },
            },
            nodes: {
              meta: {
                filtered: 2,
              },
            },
            sources: {
              meta: {
                total: 1,
              },
            },
          },
        },
      },
    },
  ]

  render(<HomeCards />, {
    withRouter: true,
    mocks,
  })

  await screen.findByRole("heading", { name: /Tables/i })

  await screen.findAllByText("38")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_COUNTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<HomeCards />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await screen.findByText("Error!")
})
