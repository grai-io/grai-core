import React from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Divider } from "@mui/material"
import FilterRows from "components/filters/FilterRows"
import { Filter } from "components/filters/filters"
import { Values } from "../FilterControl"
import FilterSave from "./FilterSave"

type AddFilterProps = {
  onClose?: () => void
  inlineFilters: Filter[]
  setInlineFilters: (filters: Filter[]) => void
  values: Values
  workspaceId: string
}

const AddFilter: React.FC<AddFilterProps> = React.forwardRef(
  ({ onClose, inlineFilters, setInlineFilters, values, workspaceId }, ref) => {
    const handleChange = (filters: Filter[]) => setInlineFilters(filters)
    const handleAdd = () =>
      setInlineFilters([
        ...inlineFilters,
        { type: "table", field: null, operator: null, value: null },
      ])

    return (
      <Box
        ref={ref}
        sx={{
          width: 750,
        }}
      >
        <Box sx={{ p: 2 }}>
          <FilterRows
            filters={inlineFilters}
            onChange={handleChange}
            namespaces={values.namespaces}
            tags={values.tags}
            sources={values.sources}
            compact
          />
        </Box>
        <Divider />
        <Box sx={{ display: "flex", p: 2 }}>
          <Button
            startIcon={<Add />}
            sx={{ color: "#8338EC" }}
            onClick={handleAdd}
          >
            Add Row
          </Button>
          <Box sx={{ flexGrow: 1 }} />
          <Button onClick={onClose}>Cancel</Button>
          <FilterSave inlineFilters={inlineFilters} workspaceId={workspaceId} />
        </Box>
      </Box>
    )
  },
)

export default AddFilter
