import { renderHook } from "@testing-library/react"
import useInlineFilters from "./useInlineFilters"
import { MemoryRouter, Route, Routes } from "react-router-dom"
import { act } from "testing"

const wrapper = ({ children }: { children: React.ReactElement }) => (
  <MemoryRouter>
    <Routes>
      <Route path="/" element={children} />
    </Routes>
  </MemoryRouter>
)

beforeEach(() => {
  window.localStorage.clear()
})

test("should return null if no inlineFilters are present", () => {
  const { result } = renderHook(() => useInlineFilters(), { wrapper })

  expect(result.current.inlineFilters).toEqual(null)
})

test("set array", async () => {
  const { result } = renderHook(() => useInlineFilters(), { wrapper })

  expect(result.current.inlineFilters).toEqual(null)

  const filter = {
    type: null,
    field: null,
    operator: null,
    value: null,
  }

  await act(async () => result.current.setInlineFilters([filter]))

  expect(result.current.inlineFilters).toEqual([filter])
})

test("set empty array", async () => {
  const { result } = renderHook(() => useInlineFilters(), { wrapper })

  expect(result.current.inlineFilters).toEqual(null)

  await act(async () => result.current.setInlineFilters([]))

  expect(result.current.inlineFilters).toEqual(null)
})
