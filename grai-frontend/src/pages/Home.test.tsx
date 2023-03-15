import React, { ReactNode } from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import Home, { GET_WORKSPACE } from "./Home"
import Workspaces, { GET_WORKSPACES } from "./workspaces/Workspaces"

jest.mock("react-instantsearch-hooks-web", () => ({
  InstantSearch: ({ children }: { children: ReactNode }) => children,
  useHits: () => ({ hits: [] }),
  useSearchBox: () => ({
    query: "",
    refine: jest.fn(),
    clear: jest.fn(),
  }),
  useInstantSearch: () => ({
    error: undefined,
  }),
}))

test("renders", async () => {
  render(<Home />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Welcome to Grai/i })
    ).toBeTruthy()
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Home />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Welcome to Grai/i })
    ).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toBeTruthy()
  })

  fireEvent.click(screen.getByRole("textbox"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toBeInTheDocument()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /close/i }))
  )
})

test("error", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})

test("missing workspace", async () => {
  const mocks = [
    profileMock,
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

  await waitFor(() => {
    expect(screen.getByRole("progressbar")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).toBeFalsy()
  })

  await waitFor(() => {
    expect(
      screen.getByRole("heading", { name: /Create a workspace/i })
    ).toBeInTheDocument()
  })
})
