import React from "react"
import { Box } from "@mui/material"

type PageContentProps = {
  children: React.ReactNode
}

const PageContent: React.FC<PageContentProps> = ({ children }) => (
  <Box
    sx={{
      backgroundColor: "white",
      m: "24px",
      p: "24px",
      borderRadius: "12px",
      boxShadow: "0px 4px 14px rgba(0, 0, 0, 0.08)",
    }}
  >
    {children}
  </Box>
)

export default PageContent
