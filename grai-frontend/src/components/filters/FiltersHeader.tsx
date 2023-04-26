import React from "react"
import { Add, Refresh } from "@mui/icons-material"
import { Box, Button, Stack, Typography } from "@mui/material"
import { Link } from "react-router-dom"

type FiltersHeaderProps = {
  onRefresh?: () => void
}

const FiltersHeader: React.FC<FiltersHeaderProps> = ({ onRefresh }) => (
  <Box sx={{ m: 3, display: "flex" }}>
    <Typography variant="h4" sx={{ flexGrow: 1 }}>
      Filters
    </Typography>
    <Stack direction="row" spacing={1}>
      <Button
        variant="outlined"
        sx={{ minWidth: 0 }}
        onClick={onRefresh}
        size="small"
        data-testid="filter-refresh"
      >
        <Refresh />
      </Button>
      <Button
        variant="outlined"
        startIcon={<Add />}
        component={Link}
        to="create"
        size="small"
      >
        Add Filter
      </Button>
    </Stack>
  </Box>
)

export default FiltersHeader
