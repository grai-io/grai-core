import React from "react"
import useTabState from "components/tabs/useTabState"
import PageContent from "./PageContent"

const PageTabs: React.FC = () => {
  const { currentTab, tabs } = useTabState()

  const tab = tabs.find(tab => tab.value === currentTab) ?? tabs[0]

  if (tab.noWrapper) return <>{tab.component}</>

  return <PageContent>{tab.component}</PageContent>
}

export default PageTabs
