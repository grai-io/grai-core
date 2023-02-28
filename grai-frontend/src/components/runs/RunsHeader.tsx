import React from "react"
import { Refresh } from "@mui/icons-material"
import { Box, Typography, Button } from "@mui/material"

type RunsHeaderProps = {
  onRefresh?: () => void
}

const RunsHeader: React.FC<RunsHeaderProps> = ({ onRefresh }) => (
  <Box sx={{ m: 3, display: "flex" }}>
    <Typography variant="h4" sx={{ flexGrow: 1 }}>
      Runs
    </Typography>
    <Button
      variant="outlined"
      sx={{ minWidth: 0 }}
      onClick={onRefresh}
      size="small"
      data-testid="connection-refresh"
    >
      <Refresh />
    </Button>
  </Box>
)

export default RunsHeader
