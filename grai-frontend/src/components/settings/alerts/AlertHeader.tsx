import React from "react"
import { Box, Typography } from "@mui/material"

interface Alert {
  id: string
  name: string
}

type AlertHeaderProps = { alert: Alert }

const AlertHeader: React.FC<AlertHeaderProps> = ({ alert }) => (
  <Box sx={{ display: "flex", mb: 3 }}>
    <Typography
      variant="h6"
      sx={{ textTransform: "uppercase", mx: 1, mt: 0.3 }}
    >
      {alert.name}
    </Typography>
  </Box>
)

export default AlertHeader
