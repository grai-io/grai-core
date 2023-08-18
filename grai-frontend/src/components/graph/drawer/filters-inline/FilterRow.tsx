import React from "react"
import FilterItem from "./FilterItem"
import { Field, Filter, Property } from "components/filters/filters"

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

  const handleFieldChange = (
    _: React.SyntheticEvent<Element, Event>,
    newValue: Field | null,
  ) => {
    let newFilter = { ...filter, field: newValue?.value ?? null }

    if (!operator && newValue?.operators && newValue?.operators.length > 0) {
      newFilter.operator = newValue?.operators[0].value
    }

    setFilter(newFilter)
  }

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
