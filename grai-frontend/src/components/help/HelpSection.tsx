import React, { ReactNode } from "react"
import { Box } from "@mui/material"

type HelpSectionProps = {
  children: ReactNode
}

const HelpSection: React.FC<HelpSectionProps> = ({ children }) => (
  <Box
    sx={{
      borderLeftWidth: 1,
      borderLeftStyle: "solid",
      borderLeftColor: "divider",
      pl: 3,
    }}
  >
    {children}
  </Box>
)

export default HelpSection
