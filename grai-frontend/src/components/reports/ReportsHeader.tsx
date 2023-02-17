import { Box, Typography } from "@mui/material"
import React from "react"

const ReportsHeader: React.FC = () => (
  <Box sx={{ m: 3, mb: 2 }}>
    <Typography variant="h4" sx={{ flexGrow: 1 }}>
      Reports
    </Typography>
  </Box>
)

export default ReportsHeader
