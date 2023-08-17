import React from "react"
import { Box, SxProps } from "@mui/material"

type PageContentProps = {
  children: React.ReactNode
  noGutter?: boolean
  noPadding?: boolean
  sx?: SxProps
}

const PageContent: React.FC<PageContentProps> = ({
  children,
  noGutter,
  noPadding,
  sx,
}) => (
  <Box
    sx={{
      backgroundColor: "white",
      my: "24px",
      mx: noGutter ? null : "24px",
      p: noPadding ? null : "24px",
      borderRadius: "12px",
      boxShadow: "0px 4px 14px rgba(0, 0, 0, 0.08)",
      ...sx,
    }}
  >
    {children}
  </Box>
)

export default PageContent
