import { GraphQLError } from "graphql"
import { render, screen } from "testing"
import ReportsCard, { GET_REPORTS } from "./ReportsCard"

test("renders", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPORTS,
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
              data: [
                {
                  id: "1",
                  status: "success",
                  connection: {
                    id: "1",
                    name: "Connection 1",
                    temp: false,
                    connector: {
                      id: "1",
                      name: "Connector 1",
                      icon: "icon",
                    },
                  },
                  commit: null,
                  created_at: "2021-01-01T00:00:00.000Z",
                  started_at: "2021-01-01T00:00:00.000Z",
                  finished_at: "2021-01-01T00:00:00.000Z",
                  user: {
                    id: "1",
                    first_name: "first",
                    last_name: "last",
                  },
                  metadata: {},
                },
              ],
            },
          },
        },
      },
    },
  ]

  render(<ReportsCard />, {
    withRouter: true,
    mocks,
  })

  await screen.findByRole("heading", { name: /Latest Reports/i })

  await screen.findAllByText("Connection 1")
})

test("empty", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPORTS,
        variables: {
          organisationName: "org",
          workspaceName: "demo",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            runs: {
              data: [],
            },
          },
        },
      },
    },
  ]

  render(<ReportsCard />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await screen.findByText(/No reports/i)
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_REPORTS,
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

  render(<ReportsCard />, {
    mocks,
    path: "/:organisationName/:workspaceName/reports",
    route: "/org/demo/reports",
  })

  await screen.findByText("Error!")
})
