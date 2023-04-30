import React from "react"
import useTabs from "helpers/useTabs"
import { TabContext } from "./TabContext"

export interface Tab {
  value: string
  label: string
  component?: React.ReactNode
  disabled?: boolean
  noWrapper?: boolean
}

type TabStateProps = {
  children?: React.ReactNode
  tabs: Tab[]
  defaultTab?: string
}

const TabState: React.FC<TabStateProps> = ({ children, tabs, defaultTab }) => {
  const { currentTab, setTab } = useTabs({ defaultTab })

  const value = {
    tabs,
    currentTab,
    setTab,
  }

  return <TabContext.Provider value={value}>{children}</TabContext.Provider>
}

export default TabState
