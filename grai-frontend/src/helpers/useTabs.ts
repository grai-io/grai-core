import useSearchParams from "./useSearchParams"

type TabsProps = {
  defaultTab?: string
  searchKey?: string
}

const useTabs = ({ defaultTab, searchKey }: TabsProps) => {
  const { searchParams, setSearchParams } = useSearchParams()

  const finalSearchKey = searchKey ?? "tab"

  const currentTab = searchParams.get(finalSearchKey) ?? defaultTab ?? null
  const setTab = (tab: string) => {
    setSearchParams({ ...searchParams, [finalSearchKey]: tab })
  }

  return { currentTab, setTab }
}

export default useTabs
