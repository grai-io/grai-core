import { useState } from "react"

const useTabs = (defaultTab: string = "") => {
  //TODO: replace with route query parameter

  const [currentTab, setTab] = useState<string>(defaultTab)

  // const currentTab = defaultTab

  // const setTab = (tab: string) => {}

  return { currentTab, setTab }
}

export default useTabs
