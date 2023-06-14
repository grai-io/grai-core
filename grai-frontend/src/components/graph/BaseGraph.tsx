import React, { useState } from "react"
import ReactFlow, {
  Controls,
  Edge,
  EdgeTypes,
  getIncomers,
  getOutgoers,
  Node,
  Position,
  ReactFlowProvider,
} from "reactflow"
import "reactflow/dist/style.css"
import Loading from "components/layout/Loading"
import BaseNode from "./BaseNode"
import GraphControls, { ControlOptions } from "./controls/GraphControls"
import GraphDetails from "./GraphDetails"
import TestEdge from "./TestEdge"

const nodeTypes = {
  baseNode: BaseNode,
}

const edgeTypes: EdgeTypes = {
  test: TestEdge,
}

const proOptions = { hideAttribution: true }

export const getAllIncomers = (
  node: Node,
  nodes: Node[],
  edges: Edge[]
): Node[] =>
  getIncomers(node, nodes, edges).reduce<Node[]>(
    (memo, incomer) =>
      incomer.id === node.id
        ? memo
        : [...memo, incomer, ...getAllIncomers(incomer, nodes, edges)],
    []
  )

export const getAllOutgoers = (
  node: Node,
  nodes: Node[],
  edges: Edge[]
): Node[] =>
  getOutgoers(node, nodes, edges).reduce<Node[]>(
    (memo, outgoer) =>
      outgoer.id === node.id
        ? memo
        : [...memo, outgoer, ...getAllOutgoers(outgoer, nodes, edges)],
    []
  )

type BaseGraphProps = {
  initialNodes: Node[]
  initialEdges: Edge[]
  expanded: string[]
  errors: boolean
  controlOptions?: ControlOptions
  search: string | null
  onSearch: (input: string | null) => void
  loading?: boolean
}

const BaseGraph: React.FC<BaseGraphProps> = ({
  initialNodes,
  initialEdges,
  expanded,
  errors,
  controlOptions,
  search,
  onSearch,
  loading,
}) => {
  const [highlighted, setHighlighted] = useState<string[]>([])

  const nodes = initialNodes.map(node => ({
    ...node,
    sourcePosition: "bottom" as Position,
    targetPosition: "top" as Position,
    type: "baseNode",
    data: {
      ...node.data,
      highlight: highlighted.includes(node.id),
    },
  }))

  const edges = initialEdges.map(edge => ({
    ...edge,
    data: {
      ...edge.data,
      highlight:
        highlighted.includes(edge.source) || highlighted.includes(edge.target),
    },
  }))

  if (!nodes) return <Loading />

  const highlightPath = (node: Node, nodes?: Node[], edges?: Edge[]) => {
    if (node && nodes && edges) {
      const allIncomers = getAllIncomers(node, nodes, edges)
      const allOutgoers = getAllOutgoers(node, nodes, edges)

      const incomerIds = allIncomers.map(i => i.id)
      const outgoerIds = allOutgoers.map(o => o.id)

      setHighlighted([node.id, ...incomerIds, ...outgoerIds])
    }
  }

  const resetNodeStyles = () => setHighlighted([])

  return (
    <ReactFlowProvider>
      <GraphControls
        errors={!!errors}
        options={controlOptions}
        search={search}
        onSearch={onSearch}
      />
      <ReactFlow
        minZoom={0}
        nodes={nodes}
        edges={edges}
        proOptions={proOptions}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodeMouseEnter={(_event, node) => highlightPath(node, nodes, edges)}
        onNodeMouseLeave={() => resetNodeStyles()}
        onPaneClick={() => {
          resetNodeStyles()
        }}
        // fitView
      >
        <Controls showInteractive={false} />
      </ReactFlow>
      {loading && <Loading />}
      <GraphDetails />
    </ReactFlowProvider>
  )
}

export default BaseGraph
