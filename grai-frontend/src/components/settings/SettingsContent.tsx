import { Box, SxProps } from "@mui/material"
import React from "react"

type SettingsContentProps = {
  children: React.ReactNode
  sx?: SxProps
}

const SettingsContent: React.FC<SettingsContentProps> = ({ children, sx }) => (
  <Box sx={{ ...sx, p: 3 }}>{children}</Box>
)

export default SettingsContent
