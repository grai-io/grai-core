import { Box } from "@mui/material"
import React from "react"
import { Edge, Node as GraphNode } from "helpers/graph"
import NodeLineage from "./NodeLineage"
import NodeProfile, { Node } from "./NodeProfile"
import Tabs from "components/tabs/Tabs"
import { BarChart, Mediation, TableRows } from "@mui/icons-material"

type NodeContentProps = {
  node: Node
  nodes: GraphNode[]
  edges: Edge[]
}

const NodeContent: React.FC<NodeContentProps> = ({ node, nodes, edges }) => (
  <Box sx={{ px: 2, py: 1 }}>
    <Tabs
      tabs={[
        {
          value: "profile",
          label: "Profile",
          icon: <BarChart />,
          element: <NodeProfile node={node} nodes={nodes} edges={edges} />,
        },
        {
          value: "sample",
          label: "Sample",
          icon: <TableRows />,
          disabled: true,
        },
        {
          value: "lineage",
          label: "Lineage",
          icon: <Mediation />,
          element: <NodeLineage node={node} />,
        },
      ]}
    />
  </Box>
)

export default NodeContent
