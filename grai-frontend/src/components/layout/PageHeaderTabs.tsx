import React from "react"
import { Tab as TabComponent, Tabs } from "@mui/material"
import useTabState from "components/tabs/useTabState"

const PageHeaderTabs: React.FC = () => {
  const { currentTab, setTab, tabs } = useTabState()

  return (
    <Tabs value={currentTab ?? tabs[0].value} sx={{ mt: "24px", mb: "-24px" }}>
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
}

export default PageHeaderTabs
