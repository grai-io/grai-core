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
  },
  {
    value: "no-parent",
    label: "No Parent",
  },
  {
    value: "child",
    label: "Has Child",
  },
  {
    value: "no-child",
    label: "No Child",
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

const tags = [
  {
    value: "grai-source-postgres",
    label: "grai-source-postgres",
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
}

const FilterRow: React.FC<FilterRowProps> = ({
  filter,
  onChange,
  onRemove,
}) => {
  return (
    <Grid container spacing={1} sx={{ mt: 0.5 }}>
      <Grid item md={3}>
        <Autocomplete
          options={types}
          value={types.find(type => type.value === filter.type) ?? null}
          onChange={(event, newValue) =>
            onChange({ ...filter, type: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
        />
      </Grid>
      <Grid item md={3}>
        <Autocomplete
          options={fields}
          value={fields.find(field => field.value === filter.field) ?? null}
          onChange={(event, newValue) =>
            onChange({ ...filter, field: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
          getOptionDisabled={option => option.disabled ?? false}
        />
      </Grid>
      <Grid item md={3}>
        <Autocomplete
          options={operators}
          value={
            operators.find(operator => operator.value === filter.operator) ??
            null
          }
          onChange={(event, newValue) =>
            onChange({ ...filter, operator: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
        />
      </Grid>
      <Grid item md={2}>
        <Autocomplete
          options={tags}
          value={tags.find(tag => tag.value === filter.value) ?? null}
          onChange={(event, newValue) =>
            onChange({ ...filter, value: newValue?.value ?? null })
          }
          renderInput={params => <TextField {...params} />}
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