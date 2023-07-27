import { useEffect } from "react"
import { useSearchParams } from "react-router-dom"
import useLocalState from "helpers/useLocalState"

const useFilters = () => {
  const [searchParams, setSearchParams] = useSearchParams()

  const searchFilters = searchParams.get("filters")?.split(",") ?? null
  const [filters, setFilters] = useLocalState<string[] | null>(
    "graph-filters",
    searchFilters,
  )

  console.log(filters)

  const handleFiltersChange = (filters: string[]) => {
    filters.length > 0 ? setFilters(filters) : setFilters(null)
  }

  useEffect(() => {
    let newParams = searchParams

    if (filters && filters.length > 0) {
      newParams.set("filters", filters.join(","))
    } else {
      newParams.delete("filters")
    }

    setSearchParams(newParams)
  }, [filters, searchParams, setSearchParams])

  return {
    filters,
    setFilters: handleFiltersChange,
  }
}

export default useFilters
