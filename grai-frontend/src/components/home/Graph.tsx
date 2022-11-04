import React from "react"
import { Edge } from "../../pages/edges/Edges"
import { Node } from "../../pages/nodes/Nodes"
import BaseGraph from "./BaseGraph"
import { Edge as RFEdge, MarkerType, Node as RFNode } from "reactflow"

type GraphProps = {
  nodes: Node[]
  edges: Edge[]
}

const position = { x: 0, y: 0 }

const Graph: React.FC<GraphProps> = ({ nodes, edges }) => {
  const initialNodes: RFNode[] = nodes.map(node => ({
    id: node.id,
    data: { id: node.id, label: node.display_name, metadata: node.metadata },
    position,
  }))

  const initialEdges: RFEdge[] = edges.map(edge => ({
    id: edge.id,
    source: edge.source,
    target: edge.destination,
    markerEnd: {
      type: MarkerType.ArrowClosed,
      width: 40,
      height: 40,
    },
  }))

  return <BaseGraph initialNodes={initialNodes} initialEdges={initialEdges} />
}

export default Graph
