import React from "react"
import { Box } from "@mui/material"
import FilterRowHeader from "components/filters/FilterRowHeader"
import FilterRow from "./FilterRow"
import { Filter, Source } from "./filters"

type FilterRowsProps = {
  filters: Filter[]
  onChange: (filters: Filter[]) => void
  namespaces: string[]
  tags: string[]
  sources: Source[]
  compact?: boolean
}

const FilterRows: React.FC<FilterRowsProps> = ({
  filters,
  onChange,
  namespaces,
  tags,
  sources,
  compact,
}) => {
  const handleChangeFilters = (index: number) => (filter: Filter) => {
    const newFilters = [...filters]
    newFilters[index] = filter
    onChange(newFilters)
  }

  const handleRemoveFilter = (index: number) => () => {
    const newFilters = [...filters]
    newFilters.splice(index, 1)
    onChange(newFilters)
  }

  return (
    <>
      {compact !== true && <FilterRowHeader />}
      <Box sx={{ mt: -1 }}>
        {filters.map((filter, index) => (
          <FilterRow
            key={index}
            filter={filter}
            onChange={handleChangeFilters(index)}
            onRemove={handleRemoveFilter(index)}
            namespaces={namespaces}
            tags={tags}
            sources={sources}
            compact={compact}
          />
        ))}
      </Box>
    </>
  )
}

export default FilterRows
