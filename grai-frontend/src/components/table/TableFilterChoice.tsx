import {
  CheckBox as CheckBoxIcon,
  CheckBoxOutlineBlank,
} from "@mui/icons-material"
import { Autocomplete, Checkbox, TextField } from "@mui/material"
import React from "react"

const icon = <CheckBoxOutlineBlank fontSize="small" />
const checkedIcon = <CheckBoxIcon fontSize="small" />

type TableFilterChoiceProps = {
  placeholder?: string
  options: string[]
  value: string[]
  onChange: (value: string[]) => void
}

const TableFilterChoice: React.FC<TableFilterChoiceProps> = ({
  placeholder,
  options,
  value,
  onChange,
}) => (
  <Autocomplete
    multiple
    value={value}
    onChange={(event, newValue) => onChange(newValue)}
    options={options}
    disableCloseOnSelect
    // getOptionLabel={(option) => option.title}
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
    size="small"
    sx={{ minWidth: 300 }}
    renderInput={params => <TextField {...params} placeholder={placeholder} />}
    data-testid="table-filter-choice"
  />
)

export default TableFilterChoice
