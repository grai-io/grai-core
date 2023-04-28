import React from "react"
import { Box, Tab, Tabs } from "@mui/material"

const ReportTabs: React.FC = () => (
  <Box sx={{ mb: "-24px", mt: "24px" }}>
    <Tabs value="graph">
      <Tab label="Graph" value="graph" />
      <Tab label="Failed" value="failed" />
      <Tab label="All" value="all" />
      <Tab label="Log" value="log" />
    </Tabs>
  </Box>
)

export default ReportTabs
