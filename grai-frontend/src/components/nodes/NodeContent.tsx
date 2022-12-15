import { Box } from "@mui/material"
import React from "react"
import { useLocation } from "react-router-dom"
import { Edge, Node as GraphNode } from "helpers/graph"
import NodeLineage from "./NodeLineage"
import NodeProfile, { Node } from "./NodeProfile"
import NodeTabs from "./NodeTabs"

type NodeContentProps = {
  node: Node
  nodes: GraphNode[]
  edges: Edge[]
}

const NodeContent: React.FC<NodeContentProps> = ({ node, nodes, edges }) => {
  const searchParams = new URLSearchParams(useLocation().search)

  const currentTab = searchParams.get("tab") ?? "profile"

  return (
    <Box sx={{ px: 2, py: 1 }}>
      <NodeTabs currentTab={currentTab} />
      {currentTab === "profile" && (
        <NodeProfile node={node} nodes={nodes} edges={edges} />
      )}
      {currentTab === "lineage" && <NodeLineage node={node} />}
    </Box>
  )
}

export default NodeContent
