import React from "react"
import {
  Autocomplete,
  AutocompleteChangeReason,
  AutocompleteCloseReason,
  Box,
  ClickAwayListener,
  Divider,
} from "@mui/material"
import theme from "theme"
import { Field, Filter } from "components/filters/filters"
import PopperComponent from "./PopperComponent"
import StyledInput from "./StyledInput"
import StyledPopper from "./StyledPopper"

type AddPopperProps = {
  anchorEl: null | HTMLElement
  setAnchorEl: (anchorEl: null | HTMLElement) => void
  fields: Field[]
  onAdd: (newFilter: Filter) => void
}

const AddPopper: React.FC<AddPopperProps> = ({
  anchorEl,
  setAnchorEl,
  fields,
  onAdd,
}) => {
  const handleClick = (
    event: React.SyntheticEvent<Element, Event>,
    value: Field | null,
    reason: AutocompleteChangeReason,
  ) => {
    const field = fields.find(field => field.value === value?.value)

    onAdd({
      type: "table",
      field: value?.value ?? null,
      operator: field?.operators[0].value ?? null,
      value: null,
    })
    handleClose()
  }

  const handleClose = () => {
    if (anchorEl) {
      anchorEl.focus()
    }
    setAnchorEl(null)
  }

  const open = Boolean(anchorEl)
  const id = open ? "github-label" : undefined

  return (
    <StyledPopper
      id={id}
      open={open}
      anchorEl={anchorEl}
      placement="bottom-start"
    >
      <ClickAwayListener onClickAway={handleClose}>
        <div>
          <Box
            sx={{
              borderBottom: `1px solid ${
                theme.palette.mode === "light" ? "#eaecef" : "#30363d"
              }`,
              padding: "8px 10px",
              fontWeight: 600,
            }}
          >
            Choose data field to add
          </Box>
          <Divider />
          <Autocomplete
            open
            onClose={(
              event: React.ChangeEvent<{}>,
              reason: AutocompleteCloseReason,
            ) => {
              if (reason === "escape") {
                handleClose()
              }
            }}
            onChange={handleClick}
            PopperComponent={PopperComponent}
            noOptionsText="No fields found"
            options={fields}
            renderInput={params => (
              <StyledInput
                ref={params.InputProps.ref}
                inputProps={params.inputProps}
                autoFocus
                placeholder="Filter Fields"
              />
            )}
          />
        </div>
      </ClickAwayListener>
    </StyledPopper>
  )
}

export default AddPopper
