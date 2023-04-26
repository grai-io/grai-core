import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Stack } from "@mui/material"
import FilterHeader from "./FilterHeader"
import FilterRow, { Filter } from "../../../filters/FilterRow"
import { LoadingButton } from "@mui/lab"

const defaultFilter: Filter = {
  type: null,
  field: null,
  operator: null,
  value: null,
}

type FilterFormProps = {
  defaultFilters?: Filter[]
  onClose?: () => void
  onSave?: (filters: Filter[]) => void
  loading?: boolean
}

const FilterForm: React.FC<FilterFormProps> = ({
  defaultFilters,
  onClose,
  onSave,
  loading,
}) => {
  const [filters, setFilters] = useState<Filter[]>(
    defaultFilters ?? [defaultFilter]
  )

  const handleAdd = () => setFilters([...filters, defaultFilter])

  const handleChange = (index: number) => (filter: Filter) => {
    const newFilters = [...filters]
    newFilters[index] = filter
    setFilters(newFilters)
  }

  const handleRemove = (index: number) => () => {
    const newFilters = [...filters]
    newFilters.splice(index, 1)
    setFilters(newFilters)
  }

  const handleSave = () => {
    console.log(filters)

    onSave && onSave(filters)
  }

  return (
    <Stack>
      <FilterHeader />
      {filters.map((filter, index) => (
        <FilterRow
          key={index}
          filter={filter}
          onChange={handleChange(index)}
          onRemove={handleRemove(index)}
        />
      ))}

      <Stack spacing={2} direction="row" sx={{ mt: 3 }}>
        <Button startIcon={<Add />} variant="outlined" onClick={handleAdd}>
          Add Filter
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        {onClose && (
          <Button variant="outlined" onClick={onClose}>
            Cancel
          </Button>
        )}
        <LoadingButton
          variant="contained"
          onClick={handleSave}
          loading={loading}
        >
          Save
        </LoadingButton>
      </Stack>
    </Stack>
  )
}

export default FilterForm
