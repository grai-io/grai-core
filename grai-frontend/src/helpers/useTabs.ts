import { useState } from "react"

const useTabs = (defaultTab: string = "") => {
  const [currentTab, setTab] = useState<string>(defaultTab)

  // const currentTab = defaultTab

  // const setTab = (tab: string) => {}

  return { currentTab, setTab }
}

export default useTabs
