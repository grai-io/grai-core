import React from "react"
import { Box, Typography } from "@mui/material"

const NotFound: React.FC = () => (
  <Box
    sx={{
      textAlign: "center",
      pt: 20,
    }}
  >
    <Typography variant="h4" sx={{ mb: 3 }}>
      Sorry something has gone wrong
    </Typography>
    <Typography variant="h4">Page not found</Typography>
  </Box>
)

export default NotFound
