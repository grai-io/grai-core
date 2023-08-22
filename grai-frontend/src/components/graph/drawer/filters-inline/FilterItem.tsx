import React, { useState } from "react"
import { Delete } from "@mui/icons-material"
import { Button, Box, Stack, Chip, IconButton, Tooltip } from "@mui/material"
import { Filter, Field, Operator } from "components/filters/filters"
import FilterPopper from "./FilterPopper"

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

  const handleClick = (event: React.MouseEvent<HTMLElement>) =>
    setAnchorEl(event.currentTarget)

  const handleDelete = (
    event: React.MouseEvent<HTMLDivElement, MouseEvent>,
  ) => {
    event.stopPropagation()
    onDelete()
  }

  const filterValueToString = (value: string | null) => {
    if (!value) return null

    if (!operator?.options) return value

    const option = operator.options.find(option =>
      typeof option === "string" ? option === value : option.value === value,
    )

    return typeof option === "string" ? option : option?.label ?? value
  }

  const filterValue = Array.isArray(filter.value)
    ? filter.value.length > 0
      ? filterValueToString(filter.value[0]) +
        (filter.value.length > 1 ? ` +${filter.value.length - 1}` : "")
      : null
    : filterValueToString(filter.value)

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
            <Tooltip title="Remove Filter">
              <IconButton size="small" component="div" onClick={handleDelete}>
                <Delete fontSize="small" />
              </IconButton>
            </Tooltip>
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
