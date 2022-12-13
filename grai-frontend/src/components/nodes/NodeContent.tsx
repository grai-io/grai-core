import { Box } from "@mui/material"
import React from "react"
import { useLocation } from "react-router-dom"
import NodeProfile, { Node } from "./NodeProfile"
import NodeTabs from "./NodeTabs"

type NodeContentProps = {
  node: Node
}

const NodeContent: React.FC<NodeContentProps> = ({ node }) => {
  const searchParams = new URLSearchParams(useLocation().search)

  const currentTab = searchParams.get("tab") ?? "profile"

  return (
    <Box sx={{ px: 2, py: 1 }}>
      <NodeTabs currentTab={currentTab} />
      {currentTab === "profile" && <NodeProfile node={node} />}
    </Box>
  )
}

export default NodeContent
