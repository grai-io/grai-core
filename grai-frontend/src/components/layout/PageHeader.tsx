import React from "react"
import { Box, SxProps, Typography } from "@mui/material"
import PageHeaderTabs, { Tab } from "./PageHeaderTabs"

type PageHeaderProps = {
  title: string
  status?: React.ReactNode
  buttons?: React.ReactNode
  tabs?: Tab[]
  currentTab?: string
  setTab?: (tab: string) => void
  sx?: SxProps
  BoxProps?: {
    sx?: SxProps
  }
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  status,
  buttons,
  tabs,
  currentTab,
  setTab,
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
    {tabs && currentTab && setTab && (
      <PageHeaderTabs tabs={tabs} currentTab={currentTab} setTab={setTab} />
    )}
  </Box>
)

export default PageHeader