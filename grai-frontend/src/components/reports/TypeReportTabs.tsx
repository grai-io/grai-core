import React from "react"
import { Box, Tab, Tabs } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"
import { Repository } from "./ReportBreadcrumbs"

type TypeReportTabsProps = {
  currentTab: string
  type: string
  repository: Repository
}

const TypeReportTabs: React.FC<TypeReportTabsProps> = ({
  currentTab,
  type,
  repository,
}) => {
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
          label="Commits"
          value="commits"
          to={`${routePrefix}/reports/${type}/${repository.owner}/${repository.repo}`}
          component={Link}
          sx={{
            minHeight: 0,
          }}
        />
        <Tab
          label="Pulls"
          value="pulls"
          to={`${routePrefix}/reports/${type}/${repository.owner}/${repository.repo}/pulls`}
          component={Link}
        />
      </Tabs>
    </Box>
  )
}

export default TypeReportTabs
