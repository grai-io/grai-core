import React from "react"
import { Delete } from "@mui/icons-material"
import {
  Box,
  Button,
  ButtonGroup,
  ClickAwayListener,
  Divider,
  IconButton,
  Tooltip,
} from "@mui/material"
import { Field, Filter, Operator } from "components/filters/filters"
import StyledPopper from "./StyledPopper"
import ValueField from "./ValueField"

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
              borderBottom: "1px solid #eaecef",
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
          <ValueField
            field={field}
            filter={filter}
            setFilter={setFilter}
            operator={operator}
            onClose={handleClose}
          />
        </div>
      </ClickAwayListener>
    </StyledPopper>
  )
}

export default FilterPopper
