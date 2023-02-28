import React, { JSXElementConstructor, ReactElement, ReactNode } from "react"
import { Box, Tab as BaseTab, Tabs as BaseTabs } from "@mui/material"
import { Link, useLocation } from "react-router-dom"

export type Tab = {
  value: string
  label: string
  icon?: string | ReactElement<any, string | JSXElementConstructor<any>>
  element?: ReactNode
  disabled?: boolean
}

type TabsProps = {
  tabs: Tab[]
  defaultTab?: string
}

const Tabs: React.FC<TabsProps> = ({ tabs, defaultTab }) => {
  const searchParams = new URLSearchParams(useLocation().search)

  const currentTab = searchParams.get("tab") ?? defaultTab ?? tabs[0].value

  return (
    <Box sx={{ px: 2, py: 1 }}>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <BaseTabs
          value={currentTab}
          sx={{
            ".MuiTabs-indicator": {
              backgroundColor: theme => theme.palette.primary.main,
            },
          }}
        >
          {tabs.map(tab => (
            <BaseTab
              key={tab.value}
              label={tab.label}
              icon={tab.icon}
              iconPosition="start"
              value={tab.value}
              to={`?tab=${tab.value}`}
              component={Link}
              disabled={tab.disabled}
              sx={{
                minHeight: 0,
              }}
            />
          ))}
        </BaseTabs>
      </Box>
      {tabs.find(tab => tab.value === currentTab)?.element ?? null}
    </Box>
  )
}

export default Tabs
