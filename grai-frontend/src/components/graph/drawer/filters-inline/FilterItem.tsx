import { VisibilityOff, Close } from "@mui/icons-material"
import { Button, Box, Stack, Chip, IconButton, Tooltip } from "@mui/material"
import React, { useState } from "react"
import FilterPopper from "./FilterPopper"
import { Filter, Field, Operator } from "components/filters/filters"

type FilterItemProps = {
  filter: Filter
  setFilter: (filter: Filter) => void
  field: Field | null
  operator: Operator | null
  onDelete: () => void
}

const FilterItem: React.FC<FilterItemProps> = ({
  filter,
  setFilter,
  field,
  operator,
  onDelete,
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [hover, setHover] = useState(false)

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    // setPendingValue(value);
    setAnchorEl(event.currentTarget)
  }

  const filterValue = Array.isArray(filter.value)
    ? filter.value.length
    : filter.value

  return (
    <>
      <Button
        fullWidth
        onClick={handleClick}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        sx={{ p: 0.5 }}
      >
        <Box
          sx={{
            display: "flex",
            width: "100%",
            justifyContent: "flex-start",
            alignItems: "center",
          }}
        >
          <Stack direction="row" spacing={0.5} sx={{ flexGrow: 1 }}>
            <Chip
              label={field?.label ?? filter.field}
              sx={{ borderRadius: 0, cursor: "pointer" }}
            />
            <Chip
              label={operator?.label ?? filter.operator}
              sx={{ borderRadius: 0, cursor: "pointer" }}
              color="success"
            />
            {filterValue && (
              <Chip
                label={filterValue}
                sx={{ borderRadius: 0, cursor: "pointer" }}
                color="info"
              />
            )}
          </Stack>
          {hover && (
            <Stack direction="row" spacing={0}>
              <Tooltip title="Ignore Filter">
                <IconButton size="small">
                  <VisibilityOff fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Remove Filter">
                <IconButton size="small" onClick={onDelete}>
                  <Close fontSize="small" />
                </IconButton>
              </Tooltip>
            </Stack>
          )}
        </Box>
      </Button>
      <FilterPopper
        anchorEl={anchorEl}
        setAnchorEl={setAnchorEl}
        filter={filter}
        setFilter={setFilter}
        field={field}
        operator={operator}
        onDelete={onDelete}
      />
    </>
  )
}

export default FilterItem
