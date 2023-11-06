import { renderHook } from "@testing-library/react"
import useFilters from "./useFilters"
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

test("should return null if no filters are present", () => {
  const { result } = renderHook(() => useFilters(), { wrapper })

  expect(result.current.filters).toEqual(null)
})

test("set array", async () => {
  const { result } = renderHook(() => useFilters(), { wrapper })

  expect(result.current.filters).toEqual(null)

  await act(async () => result.current.setFilters(["test"]))

  expect(result.current.filters).toEqual(["test"])
})

test("set empty array", async () => {
  const { result } = renderHook(() => useFilters(), { wrapper })

  expect(result.current.filters).toEqual(null)

  await act(async () => result.current.setFilters([]))

  expect(result.current.filters).toEqual(null)
})
