import React from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import FilterAutocomplete, { Option } from "./FilterAutocomplete"

type SavedFiltersProps = {
  options: Option[]
  onClose?: () => void
  onAdd?: () => void
}

const SavedFilters: React.FC<SavedFiltersProps> = React.forwardRef(
  ({ options, onClose, onAdd }, ref) => {
    const { routePrefix } = useWorkspace()

    return (
      <Box ref={ref} sx={{ width: 350 }}>
        <Box
          sx={{
            padding: "8px 10px",
            pb: 0,
            fontWeight: 600,
          }}
        >
          <Box sx={{ display: "flex", pl: "16px" }}>
            <Typography
              sx={{
                flexGrow: 1,
                pt: "10px",
                fontSize: "15px",
                fontWeight: 600,
              }}
            >
              Saved Filters
            </Typography>
            <Button
              component={Link}
              to={`${routePrefix}/filters`}
              sx={{ px: "8px", color: "#8338EC" }}
            >
              Manage
            </Button>
          </Box>
        </Box>
        <FilterAutocomplete options={options} onClose={onClose} />
        <Box sx={{ p: "16px", pt: "10px" }}>
          <Button startIcon={<Add />} sx={{ color: "#8338EC" }} onClick={onAdd}>
            Add New Filter
          </Button>
        </Box>
      </Box>
    )
  },
)

export default SavedFilters
