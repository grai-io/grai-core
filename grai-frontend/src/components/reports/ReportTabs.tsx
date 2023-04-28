import React from "react"
import { Box, Tab, Tabs } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

type ReportTabsProps = {
  currentTab: string
}

const ReportTabs: React.FC<ReportTabsProps> = ({ currentTab }) => {
  const { routePrefix } = useWorkspace()

  return (
    <Box sx={{ mb: "-24px", mt: "24px" }}>
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
