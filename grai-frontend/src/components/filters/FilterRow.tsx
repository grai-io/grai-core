import React from "react"
import { Close } from "@mui/icons-material"
import { Autocomplete, Grid, IconButton, TextField } from "@mui/material"
import FilterField from "./FilterField"

type Operator = {
  value: string
  label: string
  valueComponent?: (
    disabled: boolean,
    value: string | null,
    onChange: (value: string | null) => void,
  ) => React.ReactNode
}

type Field = {
  value: string
  label: string
  disabled?: boolean
  operators: Operator[]
}

type Property = {
  value: string
  label: string
  disabled?: boolean
  fields: Field[]
}

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
  namespaces: string[]
  tags: string[]
}

const FilterRow: React.FC<FilterRowProps> = ({
  filter,
  onChange,
  onRemove,
  namespaces,
  tags,
}) => {
  const nameField: Field = {
    value: "name",
    label: "Name",
    operators: [
      {
        value: "equals",
        label: "Equals",
      },
      {
        value: "contains",
        label: "Contains",
      },
      {
        value: "starts-with",
        label: "Starts With",
      },
      {
        value: "ends-with",
        label: "Ends With",
      },
      {
        value: "not-equals",
        label: "Not Equals",
      },
      {
        value: "not-contains",
        label: "Not Contains",
      },
    ],
  }

  const namespaceField: Field = {
    value: "namespace",
    label: "Namespace",
    operators: [
      {
        value: "in",
        label: "In",
        valueComponent: (
          disabled: boolean,
          value: string | null,
          onChange: (value: string | null) => void,
        ) => (
          <Autocomplete
            openOnFocus
            autoSelect
            disabled={disabled}
            options={namespaces}
            value={value}
            onChange={(event, newValue) => onChange(newValue)}
            renderInput={params => <TextField {...params} />}
            data-testid="autocomplete-value"
          />
        ),
      },
    ],
  }

  const sourceField: Field = {
    value: "data-source",
    label: "Data Source",
    disabled: true,
    operators: [],
  }

  const tagField: Field = {
    value: "tag",
    label: "Tag",
    operators: [
      {
        value: "contains",
        label: "Contains",
        valueComponent: (
          disabled: boolean,
          value: string | null,
          onChange: (value: string | null) => void,
        ) => (
          <Autocomplete
            openOnFocus
            autoSelect
            disabled={disabled}
            options={tags}
            value={value}
            onChange={(event, newValue) => onChange(newValue)}
            renderInput={params => <TextField {...params} />}
            data-testid="autocomplete-value"
          />
        ),
      },
    ],
  }

  // const countField: Field = {
  //   value: "count",
  //   label: "Count",
  //   disabled: true,
  //   operators: [],
  // }

  const properties: Property[] = [
    {
      value: "table",
      label: "Table",
      fields: [nameField, namespaceField, sourceField, tagField],
    },
    {
      value: "parent",
      label: "Has Parent",
      disabled: true,
      fields: [],
    },
    {
      value: "no-parent",
      label: "No Parent",
      disabled: true,
      fields: [],
    },
    {
      value: "child",
      label: "Has Child",
      disabled: true,
      fields: [],
    },
    {
      value: "no-child",
      label: "No Child",
      disabled: true,
      fields: [],
    },
    {
      value: "ancestor",
      label: "Has Ancestor",
      fields: [tagField],
    },
    {
      value: "no-ancestor",
      label: "No Ancestor",
      fields: [tagField],
    },
    {
      value: "descendant",
      label: "Has Descendant",
      fields: [tagField],
    },
    {
      value: "no-descendant",
      label: "No Descendant",
      fields: [tagField],
    },
  ]

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
            (value: string | null) => onChange({ ...filter, value }),
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
        <IconButton onClick={onRemove}>
          <Close />
        </IconButton>
      </Grid>
    </Grid>
  )
}

export default FilterRow
