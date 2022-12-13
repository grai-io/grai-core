import React, { useState } from "react"
import { Edge } from "../../pages/edges/Edges"
import { Node } from "../../pages/nodes/Nodes"
import BaseGraph, { getAllIncomers, getAllOutgoers } from "./BaseGraph"
import { Edge as RFEdge, Node as RFNode } from "reactflow"
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
  const [expanded, setExpanded] = useState<string[]>([])

  const errors: Error[] | null = searchParams.has("errors")
    ? JSON.parse(searchParams.get("errors") ?? "")
    : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const initialNodes: RFNode[] = nodes
    .filter(node => node.metadata.node_type === "Table")
    .map(node => ({
      id: node.id,
      data: {
        id: node.id,
        name: node.name,
        label: node.displayName,
        metadata: node.metadata,
        columns: nodes
          .filter(
            n =>
              (n.metadata.table_name === node.metadata.table_name ||
                `public.${n.metadata.table_name}` === node.name) &&
              n.metadata.node_type !== "Table"
          )
          .map(n => ({
            label: n.displayName ?? n.name,
          })),
        expanded: expanded.includes(node.id),
        onExpand(value: boolean) {
          setExpanded(
            value
              ? expanded.concat(node.id)
              : expanded.filter(e => e !== node.id)
          )
        },
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
        error.sourceId === edge.source.id &&
        error.destinationId === edge.destination.id
    )

    return {
      id: edge.id,
      source: edge.source.id,
      target: edge.destination.id,
      // markerEnd: {
      //   type: MarkerType.ArrowClosed,
      //   width: 40,
      //   height: 40,
      // },
      label: edgeErrors?.map(error => error.message).join(", "),
      labelStyle: { fill: "red", fontWeight: 700 },
      zIndex: 10,
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

  const transformedEdges = filteredEdges
    .map(edge => {
      const sourceNode = nodes.find(n => n.id === edge.source)
      const targetNode = nodes.find(n => n.id === edge.target)

      const sourceNodeParent = nodes.find(
        n =>
          (n.metadata.table_name === sourceNode?.metadata.table_name ||
            n.name === `public.${sourceNode?.metadata.table_name}`) &&
          n.metadata.node_type === "Table"
      )
      const targetNodeParent = nodes.find(
        n =>
          (n.metadata.table_name === targetNode?.metadata.table_name ||
            n.name === `public.${targetNode?.metadata.table_name}`) &&
          n.metadata.node_type === "Table"
      )

      const source =
        sourceNode?.metadata.node_type === "Table"
          ? edge.source
          : sourceNodeParent?.id
      const target =
        targetNode?.metadata.node_type === "Table"
          ? edge.target
          : targetNodeParent?.id

      if (!source || !target || source === target) return null

      const sourceHandle =
        sourceNodeParent && expanded.includes(sourceNodeParent?.id)
          ? sourceNode?.displayName
          : null
      const targetHandle =
        targetNodeParent && expanded.includes(targetNodeParent?.id)
          ? targetNode?.displayName
          : null

      return {
        ...edge,
        source,
        sourceHandle,
        target,
        targetHandle,
      }
    })
    .filter(notEmpty)

  // console.log(transformedEdges.filter(e => e.sourceHandle || e.targetHandle))

  return (
    <BaseGraph
      initialNodes={filteredNodes}
      initialEdges={transformedEdges}
      expanded={expanded}
    />
  )
}

export default Graph
