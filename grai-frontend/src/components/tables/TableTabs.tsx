import React from "react"
import { Box, Tab, Tabs } from "@mui/material"

const TableTabs: React.FC = () => (
  <Box sx={{ mb: "-24px", mt: "24px" }}>
    <Tabs
      value="profile"
      sx={{
        ".MuiTabs-indicator": {
          backgroundColor: theme => theme.palette.primary.main,
        },
      }}
    >
      <Tab label="Profile" value="profile" />
      <Tab label="Sample" disabled />
      <Tab label="Lineage" />
    </Tabs>
  </Box>
)

export default TableTabs
