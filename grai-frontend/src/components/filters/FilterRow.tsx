import React from "react"
import { Close } from "@mui/icons-material"
import { Box, Grid, IconButton } from "@mui/material"
import FilterField from "./FilterField"
import FilterRowValue from "./FilterRowValue"
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
  compact?: boolean
}

const FilterRow: React.FC<FilterRowProps> = ({
  filter,
  onChange,
  onRemove,
  namespaces,
  tags,
  sources,
  compact,
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
    <Box
      sx={{
        backgroundColor: compact ? "#F7F7F7" : undefined,
        p: 1,
        borderRadius: "12px",
        mt: 1,
        display: "flex",
      }}
    >
      <Grid container>
        <Grid item md={3} sx={{ pr: "6px" }}>
          <FilterField<Property>
            options={properties}
            value={property}
            onChange={(event, newValue) =>
              onChange({ ...filter, type: newValue?.value ?? null })
            }
            compact={compact}
            data-testid="autocomplete-property"
          />
        </Grid>
        <Grid item md={3} sx={{ pr: "6px" }}>
          <FilterField<Field>
            placeholder="Field"
            disabled={!property}
            options={property?.fields ?? []}
            value={field}
            onChange={handleFieldChange}
            compact={compact}
            data-testid="autocomplete-field"
          />
        </Grid>
        <Grid item md={3} sx={{ pr: "6px" }}>
          <FilterField<Operator>
            placeholder="Operator"
            disabled={!field}
            options={field?.operators ?? []}
            value={operator}
            onChange={(event, newValue) =>
              onChange({ ...filter, operator: newValue?.value ?? null })
            }
            compact={compact}
            data-testid="autocomplete-operator"
          />
        </Grid>
        <Grid item md={3}>
          <FilterRowValue
            operator={operator}
            filter={filter}
            onChange={onChange}
            compact={compact}
          />
        </Grid>
      </Grid>
      <IconButton onClick={onRemove} data-testid="filter-row-remove">
        <Close />
      </IconButton>
    </Box>
  )
}

export default FilterRow
