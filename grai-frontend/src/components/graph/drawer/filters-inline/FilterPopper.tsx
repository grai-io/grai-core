import React from "react"
import { Close, Delete, Done } from "@mui/icons-material"
import {
  Autocomplete,
  AutocompleteChangeReason,
  AutocompleteCloseReason,
  Box,
  Button,
  ButtonGroup,
  ClickAwayListener,
  Divider,
  IconButton,
  Tooltip,
} from "@mui/material"
import theme from "theme"
import arrayWrap from "helpers/arrayWrap"
import notEmpty from "helpers/notEmpty"
import {
  Field,
  Filter,
  OperationOption,
  Operator,
} from "components/filters/filters"
import PopperComponent from "./PopperComponent"
import StyledInput from "./StyledInput"
import StyledPopper from "./StyledPopper"

type FilterPopperProps = {
  anchorEl: null | HTMLElement
  setAnchorEl: (anchorEl: null | HTMLElement) => void
  filter: Filter
  setFilter: (filter: Filter) => void
  field: Field | null
  operator: Operator | null
  onDelete: () => void
}

const FilterPopper: React.FC<FilterPopperProps> = ({
  anchorEl,
  setAnchorEl,
  filter,
  setFilter,
  operator,
  field,
  onDelete,
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
    setFilter({
      ...filter,
      value: Array.isArray(newValue)
        ? newValue
            .map(option =>
              typeof option === "string" ? option : option?.value,
            )
            .filter(notEmpty)
        : (typeof newValue === "string" ? newValue : newValue?.value) ?? null,
    })

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
              display: "flex",
              alignItems: "center",
            }}
          >
            Only show Table where {field?.label ?? filter.field}
            <Box sx={{ flexGrow: 1 }} />
            <Tooltip title="Remove Filter">
              <IconButton size="small" sx={{ m: -1 }} onClick={onDelete}>
                <Delete fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
          <Box sx={{ m: 1 }}>
            <ButtonGroup size="small">
              {field?.operators.map(operator => (
                <Tooltip key={operator.value} title={operator.label}>
                  <Button
                    onClick={_ =>
                      setFilter({ ...filter, operator: operator.value })
                    }
                    variant={
                      operator.value === filter.operator
                        ? "contained"
                        : undefined
                    }
                  >
                    {operator.shortLabel ?? operator.label}
                  </Button>
                </Tooltip>
              ))}
            </ButtonGroup>
          </Box>
          <Divider />
          {operator?.options ? (
            operator.multiple ? (
              <Autocomplete<OperationOption | string, true>
                open
                multiple
                onClose={(
                  _: React.ChangeEvent<{}>,
                  reason: AutocompleteCloseReason,
                ) => {
                  if (reason === "escape") {
                    handleClose()
                  }
                }}
                value={operator.options.filter(option =>
                  arrayWrap(filter.value).includes(
                    typeof option === "string" ? option : option?.value,
                  ),
                )}
                onChange={handleValueChange}
                disableCloseOnSelect
                PopperComponent={PopperComponent}
                renderTags={() => null}
                noOptionsText={`No ${field?.label ?? filter.field}`}
                renderOption={(props, option, { selected }) => (
                  <li {...props}>
                    <Box
                      component={Done}
                      sx={{ width: 17, height: 17, mr: "5px", ml: "-2px" }}
                      style={{
                        visibility: selected ? "visible" : "hidden",
                      }}
                    />
                    <Box
                      sx={{
                        flexGrow: 1,
                        "& span": {
                          color:
                            theme.palette.mode === "light"
                              ? "#586069"
                              : "#8b949e",
                        },
                      }}
                    >
                      {typeof option === "string" ? option : option?.label}
                    </Box>
                    <Box
                      component={Close}
                      sx={{ opacity: 0.6, width: 18, height: 18 }}
                      style={{
                        visibility: selected ? "visible" : "hidden",
                      }}
                    />
                  </li>
                )}
                options={operator.options}
                getOptionLabel={option =>
                  (typeof option === "string" ? option : option?.label) ?? ""
                }
                renderInput={params => (
                  <StyledInput
                    ref={params.InputProps.ref}
                    inputProps={params.inputProps}
                    autoFocus
                    placeholder={`Filter ${filter.field}s`}
                  />
                )}
              />
            ) : (
              <Autocomplete<OperationOption | string, false>
                open
                onClose={(
                  _: React.ChangeEvent<{}>,
                  reason: AutocompleteCloseReason,
                ) => {
                  if (reason === "escape") {
                    handleClose()
                  }
                }}
                value={
                  operator.options.find(option =>
                    typeof option === "string"
                      ? option === filter.value
                      : option.value === filter.value,
                  ) ?? null
                }
                onChange={handleValueChange}
                disableCloseOnSelect
                PopperComponent={PopperComponent}
                noOptionsText={`No ${field?.label ?? filter.field}`}
                renderOption={(props, option, { selected }) => (
                  <li {...props}>
                    <Box
                      component={Done}
                      sx={{ width: 17, height: 17, mr: "5px", ml: "-2px" }}
                      style={{
                        visibility: selected ? "visible" : "hidden",
                      }}
                    />
                    <Box
                      sx={{
                        flexGrow: 1,
                        "& span": {
                          color:
                            theme.palette.mode === "light"
                              ? "#586069"
                              : "#8b949e",
                        },
                      }}
                    >
                      {typeof option === "string" ? option : option?.label}
                    </Box>
                  </li>
                )}
                options={operator.options}
                getOptionLabel={option =>
                  (typeof option === "string" ? option : option?.label) ?? ""
                }
                renderInput={params => (
                  <StyledInput
                    ref={params.InputProps.ref}
                    inputProps={params.inputProps}
                    autoFocus
                    placeholder={`Filter ${filter.field}s`}
                  />
                )}
              />
            )
          ) : (
            <StyledInput
              autoFocus
              placeholder={filter.field ?? ""}
              onChange={event =>
                setFilter({ ...filter, value: event.target.value })
              }
            />
          )}
        </div>
      </ClickAwayListener>
    </StyledPopper>
  )
}

export default FilterPopper
