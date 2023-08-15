import React from "react"
import {
  CheckBoxOutlineBlank,
  Close,
  CheckBox as CheckBoxIcon,
} from "@mui/icons-material"
import {
  Autocomplete,
  Checkbox,
  Grid,
  IconButton,
  TextField,
} from "@mui/material"
import FilterField from "./FilterField"

const icon = <CheckBoxOutlineBlank fontSize="small" />
const checkedIcon = <CheckBoxIcon fontSize="small" />

type Operator = {
  value: string
  label: string
  valueComponent?: (
    disabled: boolean,
    value: string | string[] | null,
    onChange: (value: string | string[] | null) => void,
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
  value: string | string[] | null
}

export interface Source {
  id: string
  name: string
}

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
        value: "equals",
        label: "Equals",
        valueComponent: (
          disabled: boolean,
          value: string | string[] | null,
          onChange: (value: string | string[] | null) => void,
        ) => (
          <Autocomplete
            openOnFocus
            autoSelect
            disabled={disabled}
            options={namespaces}
            value={Array.isArray(value) ? value[0] : value}
            onChange={(event, newValue) => onChange(newValue)}
            renderInput={params => <TextField {...params} />}
            data-testid="autocomplete-value"
          />
        ),
      },
      {
        value: "in",
        label: "In",
        valueComponent: (
          disabled: boolean,
          value: string | string[] | null,
          onChange: (value: string | string[] | null) => void,
        ) => (
          <Autocomplete<string, true>
            multiple
            openOnFocus
            autoSelect
            limitTags={1}
            disabled={disabled}
            options={namespaces}
            value={value ? (Array.isArray(value) ? value : [value]) : []}
            onChange={(event, newValue) => onChange(newValue)}
            renderInput={params => <TextField {...params} />}
            renderOption={(props, option, { selected }) => (
              <li {...props}>
                <Checkbox
                  icon={icon}
                  checkedIcon={checkedIcon}
                  style={{ marginRight: 8 }}
                  checked={selected}
                />
                {option}
              </li>
            )}
            data-testid="autocomplete-value"
          />
        ),
      },
    ],
  }

  const sourceField: Field = {
    value: "data-source",
    label: "Data Source",
    operators: [
      {
        value: "in",
        label: "In",
        valueComponent: (
          disabled: boolean,
          value: string | string[] | null,
          onChange: (value: string | string[] | null) => void,
        ) => (
          <Autocomplete<Source, true>
            multiple
            openOnFocus
            autoSelect
            limitTags={1}
            disabled={disabled}
            options={sources}
            value={sources.filter(source =>
              (value ? (Array.isArray(value) ? value : [value]) : []).includes(
                source.id,
              ),
            )}
            getOptionLabel={source => source.name}
            onChange={(event, newValue) =>
              onChange(newValue.map(source => source.id))
            }
            renderInput={params => <TextField {...params} />}
            renderOption={(props, option, { selected }) => (
              <li {...props}>
                <Checkbox
                  icon={icon}
                  checkedIcon={checkedIcon}
                  style={{ marginRight: 8 }}
                  checked={selected}
                />
                {option.name}
              </li>
            )}
            data-testid="autocomplete-value"
          />
        ),
      },
      {
        value: "not-in",
        label: "Not In",
        valueComponent: (
          disabled: boolean,
          value: string | string[] | null,
          onChange: (value: string | string[] | null) => void,
        ) => (
          <Autocomplete<Source, true>
            multiple
            openOnFocus
            autoSelect
            limitTags={1}
            disabled={disabled}
            options={sources}
            value={sources.filter(source =>
              (value ? (Array.isArray(value) ? value : [value]) : []).includes(
                source.id,
              ),
            )}
            getOptionLabel={source => source.name}
            onChange={(event, newValue) =>
              onChange(newValue.map(source => source.id))
            }
            renderInput={params => <TextField {...params} />}
            renderOption={(props, option, { selected }) => (
              <li {...props}>
                <Checkbox
                  icon={icon}
                  checkedIcon={checkedIcon}
                  style={{ marginRight: 8 }}
                  checked={selected}
                />
                {option.name}
              </li>
            )}
            data-testid="autocomplete-value"
          />
        ),
      },
    ],
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
          value: string | string[] | null,
          onChange: (value: string | string[] | null) => void,
        ) => (
          <Autocomplete
            openOnFocus
            autoSelect
            disabled={disabled}
            options={tags}
            value={Array.isArray(value) ? value[0] : value}
            onChange={(event, newValue) => onChange(newValue)}
            renderInput={params => <TextField {...params} />}
            data-testid="autocomplete-value"
          />
        ),
      },
      {
        value: "not-contains",
        label: "Doesn't Contain",
        valueComponent: (
          disabled: boolean,
          value: string | string[] | null,
          onChange: (value: string | string[] | null) => void,
        ) => (
          <Autocomplete
            openOnFocus
            autoSelect
            disabled={disabled}
            options={tags}
            value={Array.isArray(value) ? value[0] : value}
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
      label: "Default",
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
