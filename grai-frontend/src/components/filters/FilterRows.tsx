import React from "react"
import FilterRowHeader from "components/filters/FilterRowHeader"
import FilterRow, { Filter } from "./FilterRow"

type FilterRowsProps = {
  filters: Filter[]
  onChange: (filters: Filter[]) => void
}

const FilterRows: React.FC<FilterRowsProps> = ({ filters, onChange }) => {
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
        />
      ))}
    </>
  )
}

export default FilterRows
