import { ReactNode } from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import {
  useInstantSearch,
  useHits,
  useSearchBox,
} from "react-instantsearch-hooks"
import { act, render, screen, waitFor } from "testing"
import SearchContainer, { GET_SEARCH_KEY } from "./SearchContainer"

const onClose = jest.fn()

jest.mock("react-instantsearch-hooks", () => ({
  InstantSearch: ({ children }: { children: ReactNode }) => children,
  useHits: jest.fn(),
  useSearchBox: jest.fn(),
  useInstantSearch: jest.fn(),
}))

test("renders", async () => {
  ;(useInstantSearch as jest.Mock).mockReturnValue({
    error: undefined,
  })
  ;(useHits as jest.Mock).mockReturnValue({
    hits: [],
  })
  ;(useSearchBox as jest.Mock).mockReturnValue({
    query: "",
    refine: jest.fn(),
    clear: jest.fn(),
  })

  const user = userEvent.setup()

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    withRouter: true,
  })

  await screen.findByRole("textbox")

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))
})

test("renders results", async () => {
  ;(useInstantSearch as jest.Mock).mockReturnValue({
    error: undefined,
  })
  ;(useHits as jest.Mock).mockReturnValue({
    hits: [
      {
        id: "1",
        name: "hit1",
        display_name: "hit1_display_name",
        search_type: "Table",
      },
      {
        id: "2",
        name: "hit2",
        display_name: "hit2_display_name",
        search_type: "Column",
      },
    ],
  })
  ;(useSearchBox as jest.Mock).mockReturnValue({
    query: "test",
    refine: jest.fn(),
    clear: jest.fn(),
  })

  const user = userEvent.setup()

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    routes: ["/:organisationName/:workspaceName/nodes/:tableId"],
  })

  const textbox = screen.getByRole("textbox")

  await waitFor(() => expect(textbox).toBeTruthy())

  await act(async () => await user.type(textbox, "test"))

  await screen.findByText("hit1")

  await screen.findByText("hit2")

  await act(async () => await user.keyboard("{arrowdown}"))
  await act(async () => await user.keyboard("{arrowdown}"))
  await act(async () => await user.keyboard("{arrowup}"))
  await act(async () => await user.keyboard("{enter}"))

  await screen.findByText("New Page")
})

test("renders no results", async () => {
  ;(useInstantSearch as jest.Mock).mockReturnValue({
    error: undefined,
  })
  ;(useHits as jest.Mock).mockReturnValue({
    hits: [],
  })
  ;(useSearchBox as jest.Mock).mockReturnValue({
    query: "test",
    refine: jest.fn(),
    clear: jest.fn(),
  })

  const user = userEvent.setup()

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    withRouter: true,
  })

  await screen.findByRole("textbox")

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))

  await screen.findByText("No search results")
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

  await screen.findByText("Error!")
})

test("algolia error", async () => {
  ;(useInstantSearch as jest.Mock).mockReturnValue({
    error: Error('"validUntil" parameter expired (less than current date)'),
  })
  ;(useHits as jest.Mock).mockReturnValue({
    hits: [],
  })
  ;(useSearchBox as jest.Mock).mockReturnValue({
    query: "",
    refine: jest.fn(),
    clear: jest.fn(),
  })

  const user = userEvent.setup()

  render(<SearchContainer onClose={onClose} workspaceId="1" />, {
    withRouter: true,
  })

  await screen.findByRole("textbox")

  await act(async () => await user.type(screen.getByRole("textbox"), "test"))
})
