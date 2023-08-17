import React from "react"
import { Close } from "@mui/icons-material"
import { Grid, IconButton, TextField } from "@mui/material"
import FilterField from "./FilterField"
import {
  Field,
  Filter,
  Operator,
  Property,
  Source,
  getProperties,
} from "./filters"

type FilterRowProps = {
  filter: Filter
  onChange: (filter: Filter) => void
  onRemove: () => void
  namespaces: string[]
  tags: string[]
  sources: Source[]
}

const FilterRow: React.FC<FilterRowProps> = ({
  filter,
  onChange,
  onRemove,
  namespaces,
  tags,
  sources,
}) => {
  const properties = getProperties(namespaces, tags, sources)

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

    onChange(newFilter)
  }

  return (
    <Grid container spacing={1} sx={{ mt: 0.5 }}>
      <Grid item md={3}>
        <FilterField<Property>
          options={properties}
          value={property}
          onChange={(event, newValue) =>
            onChange({ ...filter, type: newValue?.value ?? null })
          }
          data-testid="autocomplete-property"
        />
      </Grid>
      <Grid item md={3}>
        <FilterField<Field>
          disabled={!property}
          options={property?.fields ?? []}
          value={field}
          onChange={handleFieldChange}
          data-testid="autocomplete-field"
        />
      </Grid>
      <Grid item md={3}>
        <FilterField<Operator>
          disabled={!field}
          options={field?.operators ?? []}
          value={operator}
          onChange={(event, newValue) =>
            onChange({ ...filter, operator: newValue?.value ?? null })
          }
          data-testid="autocomplete-operator"
        />
      </Grid>
      <Grid item md={2}>
        {operator?.valueComponent ? (
          operator.valueComponent(
            !operator,
            filter.value,
            (value: string | string[] | null) => onChange({ ...filter, value }),
          )
        ) : (
          <TextField
            fullWidth
            disabled={!operator}
            value={filter.value ?? ""}
            onChange={event =>
              onChange({ ...filter, value: event.target.value })
            }
            inputProps={{
              "data-testid": "value",
            }}
          />
        )}
      </Grid>
      <Grid item md={1}>
        <IconButton onClick={onRemove} data-testid="filter-row-remove">
          <Close />
        </IconButton>
      </Grid>
    </Grid>
  )
}

export default FilterRow
