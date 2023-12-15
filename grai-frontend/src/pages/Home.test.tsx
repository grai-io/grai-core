import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import { GET_COUNTS } from "components/home/HomeCards"
import { GET_REPORTS } from "components/home/ReportsCard"
import { GET_WORKSPACE_SOURCE_GRAPH } from "components/home/SourceGraph"
import Home, { GET_WORKSPACE } from "./Home"
import Workspaces, { GET_WORKSPACES } from "./workspaces/Workspaces"

window.scrollTo = jest.fn()

// jest.mock("react-instantsearch-hooks-web", () => ({
//   InstantSearch: ({ children }: { children: ReactNode }) => children,
//   useHits: () => ({ hits: [] }),
//   useSearchBox: () => ({
//     query: "",
//     refine: jest.fn(),
//     clear: jest.fn(),
//   }),
//   useInstantSearch: () => ({
//     error: undefined,
//   }),
// }))

const countsMock = {
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
            filtered: 1,
          },
        },
        nodes: {
          meta: {
            filtered: 1,
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
}

const reportsMock = {
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
          data: [],
        },
      },
    },
  },
}

const sourceGraphMock = {
  request: {
    query: GET_WORKSPACE_SOURCE_GRAPH,
    variables: {
      workspaceId: "1",
    },
  },
  result: {
    data: {
      workspace: {
        id: "1",
        source_graph: [
          {
            id: "1",
            name: "test source graph",
            icon: "test icon",
            targets: [],
          },
        ],
      },
    },
  },
}

test("renders", async () => {
  const workspaceMock = {
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
          name: "test workspace",
          sample_data: false,
          runs: {
            meta: {
              filtered: 1,
            },
          },
          nodes: {
            meta: {
              filtered: 1,
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
  }

  const mocks = [
    workspaceMock,
    workspaceMock,
    countsMock,
    countsMock,
    reportsMock,
    reportsMock,
    sourceGraphMock,
    sourceGraphMock,
  ]

  render(<Home />, {
    mocks,
    withRouter: true,
  })

  await screen.findAllByRole("heading", { name: /Welcome to Grai/i })

  await screen.findByText("test source graph")
})

// test("tour", async () => {
//   render(
//     <ShepherdTour steps={steps} tourOptions={{}}>
//       <Home />
//     </ShepherdTour>,
//     {
//       withRouter: true,
//     },
//   )

//   await waitFor(() =>
//     expect(
//       screen.getAllByRole("heading", { name: /Welcome to Grai/i }),
//     ).toBeTruthy()
//   )

//   // eslint-disable-next-line testing-library/no-wait-for-empty-callback
//   await waitFor(() => {})

//   await waitFor(() =>
//     expect(
//       screen.getByText(
//         /Follow along our tour to get started with Grai and see what it can do for you./i,
//       ),
//     ).toBeInTheDocument()
//   )

//   await act(async () => await userEvent.click(screen.getByText(/close/i)))

//   await waitFor(() =>
//     expect(
//       screen.queryByText(
//         /Follow along our tour to get started with Grai and see what it can do for you./i,
//       ),
//     ).not.toBeInTheDocument()
//   )
// })

// test("search", async () => {
//   const user = userEvent.setup()

//   render(<Home />, {
//     withRouter: true,
//   })

//   await waitFor(() =>
//     expect(
//       screen.getAllByRole("heading", { name: /Welcome to Grai/i }),
//     ).toBeTruthy()
//   )

//   await waitFor(() =>
//     expect(screen.getByRole("textbox")).toBeTruthy()
//   )

//   fireEvent.mouseDown(screen.getByRole("textbox"))

//   await waitFor(() =>
//     expect(screen.getByRole("textbox")).toBeInTheDocument()
//   )

//   await act(async () => await user.type(screen.getByRole("textbox"), "test"))

//   await act(
//     async () =>
//       await user.click(screen.getByRole("button", { name: /close/i })),
//   )
// })

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

  render(<Home />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("no workspace", async () => {
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

  render(<Home />, { mocks, withRouter: true })

  await screen.findByText("Page not found")
})

test("missing workspace", async () => {
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
        errors: [new GraphQLError("Can't find workspace")],
      },
    },
    {
      request: {
        query: GET_WORKSPACES,
      },
      result: {
        data: {
          workspaces: [],
        },
      },
    },
  ]

  render(<Home />, {
    routes: [
      {
        path: "/workspaces",
        element: <Workspaces />,
      },
    ],
    mocks,
  })

  await screen.findByRole("progressbar")

  await waitFor(() => expect(screen.queryByRole("progressbar")).toBeFalsy())

  await screen.findByRole("heading", { name: /Create an organisation/i })
})

test("no reports", async () => {
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
            name: "test workspace",
            sample_data: false,
            runs: {
              meta: {
                filtered: 0,
              },
            },
            nodes: {
              meta: {
                filtered: 0,
              },
            },
            sources: {
              meta: {
                total: 0,
              },
            },
          },
        },
      },
    },
    reportsMock,
    sourceGraphMock,
  ]

  render(<Home />, { mocks, withRouter: true })

  await screen.findAllByRole("heading", { name: /Welcome to Grai/i })

  await screen.findByRole("heading", { name: /Getting started with Grai/i })
})

test("sample data", async () => {
  const user = userEvent.setup()

  const workspaceMock = {
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
          name: "test workspace",
          sample_data: true,
          runs: {
            meta: {
              filtered: 1,
            },
          },
          nodes: {
            meta: {
              filtered: 1,
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
  }

  const mocks = [
    workspaceMock,
    workspaceMock,
    sourceGraphMock,
    sourceGraphMock,
    reportsMock,
    reportsMock,
    countsMock,
    countsMock,
  ]

  render(<Home />, { mocks, withRouter: true })

  await screen.findByText("Welcome to your new workspace")

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Get started/i })),
  )

  await waitFor(() =>
    expect(
      screen.queryByText("Welcome to your new workspace"),
    ).not.toBeInTheDocument(),
  )
})
