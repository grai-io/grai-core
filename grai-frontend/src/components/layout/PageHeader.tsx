import React from "react"
import { Box, Typography } from "@mui/material"

type PageHeaderProps = {
  title: string
}

const PageHeader: React.FC<PageHeaderProps> = ({ title }) => (
  <Box
    sx={{
      backgroundColor: "white",
      p: "24px",
      pl: "40px",
      boxShadow: "0 4px 14px 0 #00000010",
    }}
  >
    <Typography
      variant="h6"
      sx={{
        fontWeight: 800,
        fontSize: "32px",
        lineHeight: "48px",
        color: "#1F2A37",
      }}
    >
      {title}
    </Typography>
  </Box>
)

export default PageHeader
