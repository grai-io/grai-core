import React from "react"
import DangerItem from "./DangerItem"

const ClearWorkspaceCache: React.FC = () => {
  const handleClick = () => {
    if (typeof window !== "undefined" && window.localStorage) {
      window.localStorage.removeItem("graph-filters")
      window.localStorage.removeItem("graph-viewport")
    }
  }

  return (
    <DangerItem
      primary="Clear Cache"
      secondary="Clear frontend cache"
      buttonText="Clear Cache"
      onClick={handleClick}
    />
  )
}

export default ClearWorkspaceCache
