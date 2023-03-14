import React, { ReactNode } from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import SearchContainer, { GET_SEARCH_KEY } from "./SearchContainer"

const onClose = jest.fn()

jest.mock("react-instantsearch-hooks-web", () => ({
  InstantSearch: ({ children }: { children: ReactNode }) => children,
  useHits: () => ({ hits: [] }),
  useSearchBox: () => ({
    query: "",
    refine: jest.fn(),
    clear: jest.fn(),
  }),
}))

test("renders", async () => {
  const user = userEvent.setup()

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toBeTruthy()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))
})

jest.mock("react-instantsearch-hooks-web", () => ({
  InstantSearch: ({ children }: { children: ReactNode }) => children,
  useHits: () => ({
    hits: [
      {
        id: "1",
        name: "test",
        display_name: "test",
        search_type: "Table",
      },
    ],
  }),
  useSearchBox: () => ({
    query: "test",
    refine: jest.fn(),
    clear: jest.fn(),
  }),
}))

test("renders results", async () => {
  const user = userEvent.setup()

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toBeTruthy()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_SEARCH_KEY,
        variables: {
          workspaceId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
