import React, { ReactNode } from "react"
import PageContent from "./PageContent"

interface Tab {
  value: string
  component?: ReactNode
  noWrapper?: boolean
}

type PageTabsProps = {
  tabs: Tab[]
  currentTab: string
}

const PageTabs: React.FC<PageTabsProps> = ({ tabs, currentTab }) => {
  const tab = tabs.find(tab => tab.value === currentTab)

  if (!tab) return null

  if (tab.noWrapper) return <>{tab.component}</>

  return <PageContent>{tab.component}</PageContent>
}

export default PageTabs
