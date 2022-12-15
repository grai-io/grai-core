import { BarChart, TableRows, Mediation } from "@mui/icons-material"
import { Box, Tabs, Tab } from "@mui/material"
import React from "react"
import { Link } from "react-router-dom"
import theme from "theme"

type NodeTabsProps = {
  currentTab: string
}

const NodeTabs: React.FC<NodeTabsProps> = ({ currentTab }) => (
  <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
    <Tabs
      value={currentTab}
      sx={{
        ".MuiTabs-indicator": {
          backgroundColor: theme.palette.secondary.main,
        },
      }}
    >
      <Tab
        label="Profile"
        icon={<BarChart />}
        iconPosition="start"
        value="profile"
        to="?tab=profile"
        component={Link}
        sx={{
          minHeight: 0,
          "&.Mui-selected": {
            color: theme.palette.secondary.main,
          },
        }}
      />
      <Tab
        label="Sample"
        icon={<TableRows />}
        iconPosition="start"
        value="sample"
        to="?tab=sample"
        component={Link}
        sx={{
          minHeight: 0,
          "&.Mui-selected": {
            color: theme.palette.secondary.main,
          },
        }}
      />
      <Tab
        label="Lineage"
        icon={<Mediation />}
        iconPosition="start"
        value="lineage"
        to="?tab=lineage"
        component={Link}
        sx={{
          minHeight: 0,
          "&.Mui-selected": {
            color: theme.palette.secondary.main,
          },
        }}
      />
    </Tabs>
  </Box>
)

export default NodeTabs
