import React from "react"
import { Box, Tab, Tabs } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"

type ReportTabsProps = {
  currentTab: string
}

const ReportTabs: React.FC<ReportTabsProps> = ({ currentTab }) => {
  const { routePrefix } = useWorkspace()

  return (
    <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
      <Tabs
        value={currentTab}
        sx={{
          ".MuiTabs-indicator": {
            backgroundColor: theme => theme.palette.primary.main,
          },
        }}
      >
        <Tab
          label="All"
          value="all"
          to={`${routePrefix}/reports`}
          component={Link}
          sx={{
            minHeight: 0,
          }}
        />
        <Tab
          label="Pulls"
          value="pulls"
          to={`${routePrefix}/reports/pulls`}
          component={Link}
          disabled
        />
        <Tab
          label="Commits"
          value="commits"
          to={`${routePrefix}/reports/commits`}
          component={Link}
          disabled
        />
      </Tabs>
    </Box>
  )
}

export default ReportTabs
