import { Filter } from "components/filters/filters"
import useFilters from "./useFilters"
import useInlineFilters from "./useInlineFilters"

export type CombinedFilters = {
  filters: string[] | null
  setFilters: (filters: string[]) => void
  inlineFilters: Filter[] | null
  setInlineFilters: (filters: Filter[]) => void
}

const useCombinedFilters = (
  localStorageKey: string = "graph-filters",
  inlineLocalStorageKey: string = "graph-inline-filter",
  searchKey: string = "filters",
  inlineSearchKey: string = "inline-filter",
) => {
  const { filters, setFilters } = useFilters(localStorageKey, searchKey)
  const { inlineFilters, setInlineFilters } = useInlineFilters(
    inlineLocalStorageKey,
    inlineSearchKey,
  )

  const combinedFilters: CombinedFilters = {
    filters,
    setFilters,
    inlineFilters,
    setInlineFilters,
  }

  return { combinedFilters, ...combinedFilters }
}

export default useCombinedFilters
