import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Divider } from "@mui/material"
import FilterRows from "components/filters/FilterRows"
import { Filter, Source } from "components/filters/filters"

type AddFilterProps = {
  onClose?: () => void
}

const AddFilter: React.FC<AddFilterProps> = React.forwardRef(
  ({ onClose }, ref) => {
    const [filters, setFilters] = useState<Filter[]>([
      {
        type: "table",
        field: null,
        operator: null,
        value: null,
      },
    ])

    const namespaces = ["namespace1", "namespace2"]
    const tags = ["tag1", "tag2"]
    const sources: Source[] = [
      { id: "source1", name: "source1" },
      { id: "source2", name: "source2" },
    ]

    const handleChange = (filters: Filter[]) => setFilters(filters)
    const handleAdd = () =>
      setFilters([
        ...filters,
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
            filters={filters}
            onChange={handleChange}
            namespaces={namespaces}
            tags={tags}
            sources={sources}
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
          <Button
            variant="contained"
            sx={{ backgroundColor: "#8338EC", ml: 2 }}
          >
            Save Filter
          </Button>
        </Box>
      </Box>
    )
  },
)

export default AddFilter
