import React from "react"
import {
  Autocomplete,
  AutocompleteChangeReason,
  AutocompleteCloseReason,
  Box,
  ClickAwayListener,
  Divider,
  InputBase,
  Popper,
  autocompleteClasses,
  styled,
} from "@mui/material"
import theme from "theme"
import { Field, Filter } from "components/filters/filters"

interface PopperComponentProps {
  anchorEl?: any
  disablePortal?: boolean
  open: boolean
}

const StyledAutocompletePopper = styled("div")(({ theme }) => ({
  [`& .${autocompleteClasses.paper}`]: {
    boxShadow: "none",
    margin: 0,
    color: "inherit",
    fontSize: 13,
  },
  [`& .${autocompleteClasses.listbox}`]: {
    backgroundColor: theme.palette.mode === "light" ? "#fff" : "#1c2128",
    padding: 0,
    [`& .${autocompleteClasses.option}`]: {
      minHeight: "auto",
      alignItems: "flex-start",
      padding: 8,
      borderBottom: `1px solid  ${
        theme.palette.mode === "light" ? " #eaecef" : "#30363d"
      }`,
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

function PopperComponent(props: PopperComponentProps) {
  const { disablePortal, anchorEl, open, ...other } = props
  return <StyledAutocompletePopper {...other} />
}

const StyledPopper = styled(Popper)(({ theme }) => ({
  border: `1px solid ${theme.palette.mode === "light" ? "#e1e4e8" : "#30363d"}`,
  boxShadow: `0 8px 24px ${
    theme.palette.mode === "light" ? "rgba(149, 157, 165, 0.2)" : "rgb(1, 4, 9)"
  }`,
  borderRadius: 6,
  width: 300,
  zIndex: theme.zIndex.modal,
  fontSize: 13,
  color: theme.palette.mode === "light" ? "#24292e" : "#c9d1d9",
  backgroundColor: theme.palette.mode === "light" ? "#fff" : "#1c2128",
}))

const StyledInput = styled(InputBase)(({ theme }) => ({
  padding: 10,
  width: "100%",
  borderBottom: `1px solid ${
    theme.palette.mode === "light" ? "#eaecef" : "#30363d"
  }`,
  "& input": {
    borderRadius: 4,
    backgroundColor: theme.palette.mode === "light" ? "#fff" : "#0d1117",
    padding: 8,
    transition: theme.transitions.create(["border-color", "box-shadow"]),
    border: `1px solid ${
      theme.palette.mode === "light" ? "#eaecef" : "#30363d"
    }`,
    fontSize: 14,
    "&:focus": {
      boxShadow: `0px 0px 0px 3px ${
        theme.palette.mode === "light"
          ? "rgba(3, 102, 214, 0.3)"
          : "rgb(12, 45, 107)"
      }`,
      borderColor: theme.palette.mode === "light" ? "#0366d6" : "#388bfd",
    },
  },
}))

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
