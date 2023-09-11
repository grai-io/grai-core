import React from "react"
import FilterRowHeader from "components/filters/FilterRowHeader"
import FilterRow from "./FilterRow"
import { Filter, Source } from "./filters"

type FilterRowsProps = {
  filters: Filter[]
  onChange: (filters: Filter[]) => void
  namespaces: string[]
  tags: string[]
  sources: Source[]
}

const FilterRows: React.FC<FilterRowsProps> = ({
  filters,
  onChange,
  namespaces,
  tags,
  sources,
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
      <FilterRowHeader />
      {filters.map((filter, index) => (
        <FilterRow
          key={index}
          filter={filter}
          onChange={handleChangeFilters(index)}
          onRemove={handleRemoveFilter(index)}
          namespaces={namespaces}
          tags={tags}
          sources={sources}
        />
      ))}
    </>
  )
}

export default FilterRows
