/* istanbul ignore file */
import { createContext } from "react"
import { Tab } from "./TabState"

type TabContextType = {
  tabs: Tab[]
  currentTab: string | null
  setTab: (tab: string) => void
}

export const TabContext = createContext<TabContextType>({
  tabs: [],
  currentTab: null,
  setTab: () => {},
})
