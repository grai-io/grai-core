import React from "react"
import { Tab as TabComponent, Tabs } from "@mui/material"

export interface Tab {
  value: string
  label: string
  disabled?: boolean
}

type PageHeaderTabsProps = {
  tabs: Tab[]
  currentTab: string
  setTab: (tab: string) => void
}

const PageHeaderTabs: React.FC<PageHeaderTabsProps> = ({
  tabs,
  currentTab,
  setTab,
}) => (
  <Tabs value={currentTab} sx={{ mt: "24px", mb: "-24px" }}>
    {tabs.map(tab => (
      <TabComponent
        key={tab.value}
        label={tab.label}
        value={tab.value}
        onClick={() => setTab(tab.value)}
        disabled={tab.disabled}
      />
    ))}
  </Tabs>
)

export default PageHeaderTabs
