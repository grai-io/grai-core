import React from "react"
import { Edge } from "../../pages/edges/Edges"
import { Node } from "../../pages/nodes/Nodes"
import BaseGraph, { getAllIncomers, getAllOutgoers } from "./BaseGraph"
import { Edge as RFEdge, MarkerType, Node as RFNode } from "reactflow"
import { useLocation } from "react-router-dom"

interface Error {
  source: string
  destination: string
  test: string
  message: string
}

type GraphProps = {
  nodes: Node[]
  edges: Edge[]
}

const position = { x: 0, y: 0 }

const Graph: React.FC<GraphProps> = ({ nodes, edges }) => {
  const searchParams = new URLSearchParams(useLocation().search)

  const errors: Error[] | null = searchParams.has("errors")
    ? JSON.parse(searchParams.get("errors") ?? "")
    : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const initialNodes: RFNode[] = nodes.map(node => ({
    id: node.id,
    data: {
      id: node.id,
      name: node.name,
      label: node.display_name,
      metadata: node.metadata,
    },
    position,
  }))

  const nameToNode = (name: string) => nodes.find(n => n.name === name)

  const enrichedErrors = errors?.map(error => ({
    ...error,
    sourceId: nameToNode(error.source)?.id,
    destinationId: nameToNode(error.destination)?.id,
  }))

  const initialEdges: RFEdge[] = edges.map(edge => {
    const edgeErrors = enrichedErrors?.filter(
      error =>
        error.sourceId === edge.source &&
        error.destinationId === edge.destination
    )

    return {
      id: edge.id,
      source: edge.source,
      target: edge.destination,
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 40,
        height: 40,
      },
      label: edgeErrors?.map(error => error.message).join(", "),
      labelStyle: { fill: "red", fontWeight: 700 },
    }
  })

  function notEmpty<TValue>(value: TValue | null | undefined): value is TValue {
    return value !== null && value !== undefined
  }

  const errorIds: string[] =
    enrichedErrors?.map(e => e.destinationId).filter(notEmpty) ?? []

  const filteredNodes = limitGraph
    ? initialNodes.filter(
        node =>
          getAllOutgoers(node, initialNodes, initialEdges).filter(n =>
            errorIds?.includes(n.id)
          ).length > 0 ||
          getAllIncomers(node, initialNodes, initialEdges).filter(n =>
            errorIds?.includes(n.id)
          ).length > 0 ||
          errorIds?.includes(node.id)
      )
    : initialNodes

  const filteredNodesIds = filteredNodes.map(n => n.id)

  const filteredEdges = limitGraph
    ? initialEdges.filter(
        edge =>
          filteredNodesIds.includes(edge.source) &&
          filteredNodesIds.includes(edge.target)
      )
    : initialEdges

  return <BaseGraph initialNodes={filteredNodes} initialEdges={filteredEdges} />
}

export default Graph
