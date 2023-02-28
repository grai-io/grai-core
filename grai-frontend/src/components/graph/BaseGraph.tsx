import React, { useState, useEffect } from "react"
import Elk, { ElkNode } from "elkjs"
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
import TestEdge from "./TestEdge"

const DEFAULT_WIDTH = 300
const DEFAULT_HEIGHT = 110

const nodeTypes = {
  baseNode: BaseNode,
}

const edgeTypes: EdgeTypes = {
  test: TestEdge,
}

export const createGraphLayout = async (
  initialNodes: Node[],
  initialEdges: Edge[]
) => {
  const nodes: ElkNode[] = []
  const edges: any[] = []

  const elk = new Elk({
    defaultLayoutOptions: {
      "elk.algorithm": "layered",
      // "elk.direction": "RIGHT",
      "elk.padding": "[top=200,left=100,bottom=25,right=25]",
      "elk.spacing.nodeNode": "100",
      "elk.layered.spacing.nodeNodeBetweenLayers": "250",
      "elk.edgeRouting": "SPLINES",
    },
  })

  initialNodes.forEach(node =>
    nodes.push({
      id: node.id,
      width: DEFAULT_WIDTH,
      height:
        DEFAULT_HEIGHT +
        (node.data.expanded ? node.data.columns.length * 42 + 100 : 0),
    })
  )

  initialEdges.forEach(edge =>
    edges.push({
      id: edge.id,
      target: edge.target,
      source: edge.source,
    })
  )

  const newGraph = await elk.layout({
    id: "root",
    children: nodes,
    edges,
  })

  return initialNodes.map(node => {
    const gnode = newGraph?.children?.find(n => n.id === node.id)
    node.sourcePosition = "bottom" as Position
    node.targetPosition = "top" as Position
    node.type = "baseNode"
    if (gnode?.x && gnode?.y && gnode?.width && gnode?.height) {
      node.position = {
        x: gnode.x - gnode.width / 2 + Math.random() / 1000,
        y: gnode.y - gnode.height / 2 + (node.data.expanded ? 120 : 0),
      }
    }

    return node
  })
}

const proOptions = { hideAttribution: true }

export const getAllIncomers = (
  node: Node,
  nodes: Node[],
  edges: Edge[]
): Node[] => {
  return getIncomers(node, nodes, edges).reduce<Node[]>(
    (memo, incomer) => [
      ...memo,
      incomer,
      ...getAllIncomers(incomer, nodes, edges),
    ],
    []
  )
}

export const getAllOutgoers = (
  node: Node,
  nodes: Node[],
  edges: Edge[]
): Node[] => {
  return getOutgoers(node, nodes, edges).reduce<Node[]>(
    (memo, outgoer) => [
      ...memo,
      outgoer,
      ...getAllOutgoers(outgoer, nodes, edges),
    ],
    []
  )
}

type BaseGraphProps = {
  initialNodes: Node[]
  initialEdges: Edge[]
  expanded: string[]
  errors: boolean
  controlOptions?: ControlOptions
  search: string | null
  onSearch: (input: string | null) => void
}

const BaseGraph: React.FC<BaseGraphProps> = ({
  initialNodes,
  initialEdges,
  expanded,
  errors,
  controlOptions,
  search,
  onSearch,
}) => {
  const [nodes, setNodes] = useState<Node[]>()
  const [edges, setEdges] = useState<Edge[]>(initialEdges)

  useEffect(() => {
    createGraphLayout(initialNodes, initialEdges)
      .then(res => {
        setNodes(res)
        setEdges(initialEdges)
      })
      .catch(err => console.error(err))
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
        prevEdges.map(elem => {
          const highlight =
            incomerIds.includes(elem.target) ||
            (incomerIds.includes(elem.source) && node.id === elem.target) ||
            (outgoerIds.includes(elem.target) && node.id === elem.source) ||
            outgoerIds.includes(elem.source)

          elem.style = {
            ...elem.style,
            stroke: highlight ? theme.palette.primary.contrastText : undefined,
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

    setEdges((prevEdges: Edge[]) =>
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
        fitView
      >
        <Controls showInteractive={false} />
      </ReactFlow>
    </ReactFlowProvider>
  )
}

export default BaseGraph
