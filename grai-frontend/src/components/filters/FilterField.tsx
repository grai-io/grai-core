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
  > {}

const FilterField = <T extends Field>(props: FilterFieldProps<T>) => (
  <Autocomplete
    {...props}
    openOnFocus
    autoSelect
    renderInput={params => <TextField {...params} />}
    getOptionDisabled={option => option.disabled ?? false}
  />
)

export default FilterField
