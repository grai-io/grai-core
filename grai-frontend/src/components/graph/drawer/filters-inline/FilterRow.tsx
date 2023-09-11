import React from "react"
import { Filter, Property } from "components/filters/filters"
import FilterItem from "./FilterItem"

type FilterRowProps = {
  properties: Property[]
  filter: Filter
  setFilter: (filter: Filter) => void
  onDelete: () => void
}

const FilterRow: React.FC<FilterRowProps> = ({
  properties,
  filter,
  setFilter,
  onDelete,
}) => {
  const property =
    properties.find(property => property.value === filter.type) ?? null
  const field =
    property?.fields.find(field => field.value === filter.field) ?? null
  const operator =
    field?.operators.find(operator => operator.value === filter.operator) ??
    null

  return (
    <FilterItem
      onDelete={onDelete}
      filter={filter}
      setFilter={setFilter}
      field={field}
      operator={operator}
    />
  )
}

export default FilterRow
