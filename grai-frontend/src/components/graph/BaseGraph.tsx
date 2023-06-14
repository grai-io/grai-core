import React, { useState, useEffect } from "react"
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
import theme from "theme"
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
  const [nodes, setNodes] = useState<Node[]>()
  const [edges, setEdges] = useState<Edge[] | undefined>(initialEdges)

  useEffect(() => {
    setEdges(initialEdges)
    setNodes(
      initialNodes.map(node => ({
        ...node,
        sourcePosition: "bottom" as Position,
        targetPosition: "top" as Position,
        type: "baseNode",
      }))
    )
  }, [initialNodes, initialEdges, expanded])

  if (!nodes) return <Loading />

  const highlightPath = (node: Node, nodes?: Node[], edges?: Edge[]) => {
    if (node && nodes && edges) {
      const allIncomers = getAllIncomers(node, nodes, edges)
      const allOutgoers = getAllOutgoers(node, nodes, edges)

      const incomerIds = allIncomers.map(i => i.id)
      const outgoerIds = allOutgoers.map(o => o.id)

      setNodes(prevNodes =>
        prevNodes?.map(elem => {
          if (allOutgoers.length > 0 || allIncomers.length > 0) {
            const highlight =
              elem.id === node.id ||
              incomerIds.includes(elem.id) ||
              outgoerIds.includes(elem.id)

            elem.data.highlight = highlight
          }

          return elem
        })
      )

      setEdges(prevEdges =>
        prevEdges?.map(elem => {
          const highlight =
            incomerIds.includes(elem.target) ||
            (incomerIds.includes(elem.source) && node.id === elem.target) ||
            (outgoerIds.includes(elem.target) && node.id === elem.source) ||
            outgoerIds.includes(elem.source)

          elem.style = {
            ...elem.style,
            stroke: highlight ? theme.palette.secondary.main : undefined,
          }

          return elem
        })
      )
    }
  }

  const resetNodeStyles = () => {
    setNodes(prevNodes =>
      prevNodes?.map(node => {
        node.data.highlight = false
        node.style = {
          ...node.style,
          opacity: 1,
        }

        return node
      })
    )

    setEdges((prevEdges: Edge[] | undefined) =>
      prevEdges?.map(edge => {
        edge.animated = false
        edge.style = {
          ...edge.style,
          stroke: "#b1b1b7",
          opacity: 1,
        }

        return edge
      })
    )
  }

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
