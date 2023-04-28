import React from "react"
import { Close } from "@mui/icons-material"
import { Autocomplete, Grid, IconButton, TextField } from "@mui/material"

const types = [
  {
    value: "table",
    label: "Table",
  },
  {
    value: "parent",
    label: "Has Parent",
    disabled: true,
  },
  {
    value: "no-parent",
    label: "No Parent",
    disabled: true,
  },
  {
    value: "child",
    label: "Has Child",
    disabled: true,
  },
  {
    value: "no-child",
    label: "No Child",
    disabled: true,
  },
  {
    value: "ancestor",
    label: "Has Ancestor",
  },
  {
    value: "no-ancestor",
    label: "No Ancestor",
  },
  {
    value: "descendant",
    label: "Has Descendant",
  },
  {
    value: "no-descendant",
    label: "No Descendant",
  },
]

const fields = [
  {
    value: "name",
    label: "Name",
    disabled: true,
  },
  {
    value: "data-source",
    label: "Data Source",
    disabled: true,
  },
  {
    value: "tag",
    label: "Tag",
  },
  {
    value: "count",
    label: "Count",
    disabled: true,
  },
]

const operators = [
  {
    value: "contains",
    label: "Contains",
  },
]

export type Filter = {
  type: string | null
  field: string | null
  operator: string | null
  value: string | null
}

type FilterRowProps = {
  filter: Filter
  onChange: (filter: Filter) => void
  onRemove: () => void
  tags: string[]
}

const FilterRow: React.FC<FilterRowProps> = ({
  filter,
  onChange,
  onRemove,
  tags,
}) => {
  return (
    <Grid container spacing={1} sx={{ mt: 0.5 }}>
      <Grid item md={3}>
        <Autocomplete
          openOnFocus
          autoSelect
          options={types}
          value={types.find(type => type.value === filter.type) ?? null}
          onChange={(event, newValue) =>
            onChange({ ...filter, type: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
          getOptionDisabled={option => option.disabled ?? false}
          data-testid="autocomplete-property"
        />
      </Grid>
      <Grid item md={3}>
        <Autocomplete
          openOnFocus
          autoSelect
          options={fields}
          value={fields.find(field => field.value === filter.field) ?? null}
          onChange={(event, newValue) =>
            onChange({ ...filter, field: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
          getOptionDisabled={option => option.disabled ?? false}
          data-testid="autocomplete-field"
        />
      </Grid>
      <Grid item md={3}>
        <Autocomplete
          openOnFocus
          autoSelect
          options={operators}
          value={
            operators.find(operator => operator.value === filter.operator) ??
            null
          }
          onChange={(event, newValue) =>
            onChange({ ...filter, operator: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
          data-testid="autocomplete-operator"
        />
      </Grid>
      <Grid item md={2}>
        <Autocomplete
          openOnFocus
          autoSelect
          options={tags}
          value={filter.value ?? null}
          onChange={(event, newValue) =>
            onChange({ ...filter, value: newValue })
          }
          renderInput={params => <TextField {...params} />}
          data-testid="autocomplete-value"
        />
      </Grid>
      <Grid item md={1}>
        <IconButton onClick={onRemove}>
          <Close />
        </IconButton>
      </Grid>
    </Grid>
  )
}

export default FilterRow
