import React from "react"
import { Box, Typography } from "@mui/material"

type SettingsAppBarProps = {
  title: string
  buttons?: React.ReactNode
}

const SettingsAppBar: React.FC<SettingsAppBarProps> = ({ title, buttons }) => (
  <Box
    sx={{
      px: "48px",
      py: "16px",
      borderBottomStyle: "solid",
      borderBottomWidth: 1,
      borderBottomColor: "divider",
      display: "flex",
    }}
  >
    <Typography
      variant="h6"
      component="div"
      sx={{
        color: "rgba(0, 0, 0, 0.80)",
        fontSize: "24px",
        fontWeight: 400,
        lineHeight: "32px",
        my: "8px",
      }}
    >
      {title}
    </Typography>
    <Box sx={{ flexGrow: 1 }} />
    {buttons}
  </Box>
)

export default SettingsAppBar
