import React, { ReactNode } from "react"
import { Box, Typography, Divider } from "@mui/material"

type HelpItemProps = {
  title: string
  children?: ReactNode
}

const HelpItem: React.FC<HelpItemProps> = ({ title, children }) => (
  <Box sx={{ mb: 5 }}>
    <Typography>{title}</Typography>
    <Divider sx={{ my: 1 }} />
    <Typography variant="body2">{children}</Typography>
  </Box>
)

export default HelpItem
