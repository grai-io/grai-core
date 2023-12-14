import { useEffect } from "react"
import { useSearchParams } from "react-router-dom"
import useLocalState from "helpers/useLocalState"
import { Filter } from "components/filters/filters"

const useInlineFilters = (
  localStorageKey: string = "graph-inline-filter",
  searchKey: string = "inline-filter",
) => {
  const [searchParams, setSearchParams] = useSearchParams()

  const searchValue = searchParams.get(searchKey)
  const searchFilters: Filter[] | null = searchValue
    ? JSON.parse(searchValue)
    : null

  const [filters, setFilters] = useLocalState<Filter[] | null>(
    localStorageKey,
    searchFilters,
    true,
  )

  const handleFiltersChange = (filters: Filter[]) => {
    filters.length > 0 ? setFilters(filters) : setFilters(null)
  }

  useEffect(() => {
    let newParams = searchParams

    if (filters && filters.length > 0) {
      newParams.set(searchKey, JSON.stringify(filters))
    } else {
      newParams.delete(searchKey)
    }

    setSearchParams(newParams)
  }, [searchKey, filters, searchParams, setSearchParams])

  return {
    inlineFilters: filters,
    setInlineFilters: handleFiltersChange,
  }
}

export default useInlineFilters
