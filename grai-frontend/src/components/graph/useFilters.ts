import { useEffect } from "react"
import { useSearchParams } from "react-router-dom"
import useLocalState from "helpers/useLocalState"

const useFilters = (
  localStorageKey: string = "graph-filters",
  searchKey: string = "filters",
) => {
  const [searchParams, setSearchParams] = useSearchParams()

  const searchFilters = searchParams.get(searchKey)?.split(",") ?? null
  const [filters, setFilters] = useLocalState<string[] | null>(
    localStorageKey,
    searchFilters,
    true,
  )

  const handleFiltersChange = (filters: string[]) => {
    filters.length > 0 ? setFilters(filters) : setFilters(null)
  }

  useEffect(() => {
    let newParams = searchParams

    if (filters && filters.length > 0) {
      newParams.set(searchKey, filters.join(","))
    } else {
      newParams.delete(searchKey)
    }

    setSearchParams(newParams)
  }, [searchKey, filters, searchParams, setSearchParams])

  return {
    filters,
    setFilters: handleFiltersChange,
  }
}

export default useFilters
