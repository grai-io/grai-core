import React from "react"
import { Box, SxProps, Typography } from "@mui/material"
import PageHeaderTabs from "./PageHeaderTabs"

type PageHeaderProps = {
  title?: string
  breadcrumbs?: React.ReactNode
  status?: React.ReactNode
  buttons?: React.ReactNode
  tabs?: boolean
  children?: React.ReactNode
  sx?: SxProps
  BoxProps?: {
    sx?: SxProps
  }
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  breadcrumbs,
  status,
  buttons,
  tabs,
  children,
  sx,
  BoxProps,
}) => (
  <Box
    sx={{
      backgroundColor: "white",
      p: "24px",
      pl: "40px",
      boxShadow: "0 4px 14px 0 #00000010",
      ...sx,
    }}
  >
    {breadcrumbs && <Box sx={{ mt: -1, mb: 2 }}> {breadcrumbs} </Box>}
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        ...BoxProps?.sx,
      }}
    >
      <Typography
        variant="h6"
        sx={{
          fontWeight: 800,
          fontSize: "32px",
          lineHeight: "48px",
          color: "#1F2A37",
          mr: 3,
        }}
      >
        {title}
      </Typography>
      {status}
      <Box sx={{ flexGrow: 1 }} />
      <Box>{buttons}</Box>
    </Box>
    {children}
    {tabs && <PageHeaderTabs />}
  </Box>
)

export default PageHeader
