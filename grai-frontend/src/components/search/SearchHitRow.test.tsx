import React, { ReactNode } from "react"
import { render } from "testing"
import SearchHitRow from "./SearchHitRow"

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

test("renders table", async () => {
  const hit = {
    objectID: "1",
    id: "1",
    name: "test",
    display_name: "test",
    search_type: "Table",
  }

  render(<SearchHitRow hit={hit} />, {
    withRouter: true,
  })
})

test("renders column", async () => {
  const hit = {
    objectID: "1",
    id: "1",
    name: "test",
    display_name: "test",
    search_type: "Column",
  }

  render(<SearchHitRow hit={hit} />, {
    withRouter: true,
  })
})

test("renders other", async () => {
  const hit = {
    objectID: "1",
    id: "1",
    name: "test",
    display_name: "test",
    search_type: "Node",
  }

  render(<SearchHitRow hit={hit} />, {
    withRouter: true,
  })
})
