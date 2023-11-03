import React from "react"
import { CheckBox, CheckBoxOutlineBlank } from "@mui/icons-material"
import {
  Autocomplete,
  AutocompleteCloseReason,
  Checkbox,
  InputBase,
  autocompleteClasses,
  styled,
} from "@mui/material"

interface PopperComponentProps {
  anchorEl?: any
  disablePortal?: boolean
  open: boolean
}

const StyledInput = styled(InputBase)(({ theme }) => ({
  padding: 10,
  paddingLeft: "16px",
  paddingRight: "16px",
  width: "100%",
  "& input": {
    borderRadius: 4,
    backgroundColor: "#fff",
    padding: 8,
    transition: theme.transitions.create(["border-color", "box-shadow"]),
    border: "1px solid #eaecef",
    fontSize: 14,
    "&:focus": {
      boxShadow: "0px 0px 0px 3px rgba(3, 102, 214, 0.3)",
      borderColor: "#0366d6",
    },
  },
}))

function PopperComponent(props: PopperComponentProps) {
  const { disablePortal, anchorEl, open, ...other } = props
  return <StyledAutocompletePopper {...other} />
}

const StyledAutocompletePopper = styled("div")(({ theme }) => ({
  [`& .${autocompleteClasses.paper}`]: {
    boxShadow: "none",
    margin: 0,
    color: "inherit",
    fontSize: 13,
  },
  [`& .${autocompleteClasses.listbox}`]: {
    backgroundColor: "#fff",
    padding: "16px",
    paddingTop: 0,
    paddingBottom: 0,
    [`& .${autocompleteClasses.option}`]: {
      padding: 2,
      borderBottom: "1px solid #eaecef",
      '&[aria-selected="true"]': {
        backgroundColor: "transparent",
      },
      [`&.${autocompleteClasses.focused}, &.${autocompleteClasses.focused}[aria-selected="true"]`]:
        {
          backgroundColor: theme.palette.action.hover,
        },
    },
  },
  [`&.${autocompleteClasses.popperDisablePortal}`]: {
    position: "relative",
  },
}))

const icon = <CheckBoxOutlineBlank fontSize="small" />
const checkedIcon = <CheckBox fontSize="small" />

export type Option = {
  value: string
  label: string | null
}

type FilterAutocompleteProps = {
  options: Option[]
  onClose?: () => void
  filters: string[]
  setFilters: (filters: string[]) => void
}

const FilterAutocomplete: React.FC<FilterAutocompleteProps> = ({
  options,
  onClose,
  filters,
  setFilters,
}) => {
  const value = options.filter(option => filters.includes(option.value))

  return (
    <Autocomplete<Option, true>
      open
      multiple
      onClose={(
        event: React.ChangeEvent<{}>,
        reason: AutocompleteCloseReason,
      ) => {
        if (reason === "escape") {
          onClose && onClose()
        }
      }}
      value={value}
      onChange={(event, newValue, reason) =>
        setFilters(newValue.map(option => option.value))
      }
      disableCloseOnSelect
      PopperComponent={PopperComponent}
      noOptionsText="No filters found"
      options={options}
      getOptionLabel={option => option.label || option.value}
      renderOption={(props, option, { selected }) => (
        <li {...props}>
          <Checkbox icon={icon} checkedIcon={checkedIcon} checked={selected} />
          {option.label}
        </li>
      )}
      renderInput={params => (
        <StyledInput
          ref={params.InputProps.ref}
          inputProps={params.inputProps}
          autoFocus
          placeholder="Search filters"
        />
      )}
    />
  )
}

export default FilterAutocomplete
