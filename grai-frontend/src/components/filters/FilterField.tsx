import React from "react"
import { Autocomplete, AutocompleteProps, TextField } from "@mui/material"

interface Field {
  value: string
  label: string
  disabled?: boolean
}

interface FilterFieldProps<T extends Field>
  extends Omit<
    AutocompleteProps<T, false, false, false, "div">,
    "renderInput"
  > {
  placeholder?: string
  compact?: boolean
}

const FilterField = <T extends Field>({
  compact,
  placeholder,
  ...rest
}: FilterFieldProps<T>) => (
  <Autocomplete
    {...rest}
    openOnFocus
    autoSelect
    renderInput={params => (
      <TextField
        {...params}
        sx={{ backgroundColor: "white" }}
        size={compact ? "small" : undefined}
        placeholder={placeholder}
      />
    )}
    getOptionDisabled={option => option.disabled ?? false}
    disablePortal={compact}
  />
)

export default FilterField
