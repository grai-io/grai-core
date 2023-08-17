import { Add, Save } from "@mui/icons-material"
import { Box, Button, Stack } from "@mui/material"
import React from "react"
import FilterRow from "./filters-inline/FilterRow"

const GraphFilterTextbox: React.FC = () => {
  return (
    <>
      <Box sx={{ p: 1 }}>
        <Stack direction="row" spacing={1}>
          <Button variant="outlined" fullWidth startIcon={<Add />}>
            Add Field
          </Button>
          <Button variant="outlined" fullWidth startIcon={<Save />}>
            Save
          </Button>
        </Stack>
      </Box>
      <Box sx={{ p: 1 }}>
        <FilterRow />
        <FilterRow />
      </Box>
    </>
  )
}

export default GraphFilterTextbox
