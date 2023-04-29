import { useContext } from "react"
import { TabContext } from "./TabContext"

const useTabState = () => useContext(TabContext)

export default useTabState
