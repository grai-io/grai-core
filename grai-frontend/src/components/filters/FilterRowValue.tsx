import React from "react"
import { CheckBox, CheckBoxOutlineBlank } from "@mui/icons-material"
import {
  Autocomplete,
  AutocompleteChangeReason,
  Checkbox,
  TextField,
} from "@mui/material"
import arrayFirst from "helpers/arrayFirst"
import arrayWrap from "helpers/arrayWrap"
import notEmpty from "helpers/notEmpty"
import { Filter, OperationOption, Operator } from "./filters"

const icon = <CheckBoxOutlineBlank fontSize="small" />
const checkedIcon = <CheckBox fontSize="small" />

type FilterRowValueProps = {
  operator: Operator | null
  filter: Filter
  onChange: (filter: Filter) => void
  compact?: boolean
}

const FilterRowValue: React.FC<FilterRowValueProps> = ({
  operator,
  filter,
  onChange,
  compact,
}) => {
  const handleValueChange = (
    event: React.SyntheticEvent<Element, Event>,
    newValue:
      | null
      | string
      | OperationOption
      | (null | string | OperationOption)[],
    reason: AutocompleteChangeReason,
  ) =>
    onChange({
      ...filter,
      value: Array.isArray(newValue)
        ? newValue
            .map(option =>
              typeof option === "string" ? option : option?.value,
            )
            .filter(notEmpty)
        : (typeof newValue === "string" ? newValue : newValue?.value) ?? null,
    })

  if (!operator?.options)
    return (
      <TextField
        fullWidth
        disabled={!operator}
        value={filter.value ?? ""}
        onChange={event => onChange({ ...filter, value: event.target.value })}
        inputProps={{
          "data-testid": "value",
        }}
        size={compact ? "small" : undefined}
        placeholder={compact ? "Value" : undefined}
        sx={{ backgroundColor: "white" }}
      />
    )

  if (operator.multiple)
    return (
      <Autocomplete<string | OperationOption, true>
        multiple
        openOnFocus
        autoSelect
        limitTags={1}
        options={operator.options}
        value={operator.options.filter(option =>
          arrayWrap(filter.value).includes(
            typeof option === "string" ? option : option?.value,
          ),
        )}
        onChange={handleValueChange}
        renderInput={params => (
          <TextField
            {...params}
            sx={{ backgroundColor: "white" }}
            placeholder={compact ? "Value" : undefined}
          />
        )}
        renderOption={(props, option, { selected }) => (
          <li {...props}>
            <Checkbox
              icon={icon}
              checkedIcon={checkedIcon}
              style={{ marginRight: 8 }}
              checked={selected}
            />
            {typeof option === "string" ? option : option?.label}
          </li>
        )}
        size={compact ? "small" : undefined}
        disablePortal={compact}
        data-testid="autocomplete-value"
      />
    )

  return (
    <Autocomplete<string | OperationOption, false>
      openOnFocus
      autoSelect
      disabled={!operator}
      options={operator.options}
      value={arrayFirst(filter.value)}
      onChange={handleValueChange}
      renderInput={params => (
        <TextField
          {...params}
          sx={{ backgroundColor: "white" }}
          placeholder={compact ? "Value" : undefined}
        />
      )}
      size={compact ? "small" : undefined}
      disablePortal={compact}
      data-testid="autocomplete-value"
    />
  )
}

export default FilterRowValue
