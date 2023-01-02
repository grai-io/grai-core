import React, { useState } from "react"
import BaseGraph, { getAllIncomers, getAllOutgoers } from "./BaseGraph"
import { Edge as RFEdge, Node as RFNode } from "reactflow"
import notEmpty from "helpers/notEmpty"
import { Table, Node as NodeType } from "helpers/graph"

export interface Error {
  source: string
  destination: string
  test: string
  message: string
}

interface Edge {
  id: string
  data_source: string
  is_active: boolean
  source: Node
  destination: Node
  metadata: any
}

interface Node extends NodeType {
  display_name: string
}

type GraphProps = {
  tables: Table<Node>[]
  edges: Edge[]
  errors?: Error[] | null
  limitGraph?: boolean
  initialHidden?: string[]
}

const position = { x: 0, y: 0 }

const Graph: React.FC<GraphProps> = ({
  tables,
  edges,
  errors,
  limitGraph,
  initialHidden,
}) => {
  const [hidden, setHidden] = useState<string[]>(initialHidden ?? [])
  const [expanded, setExpanded] = useState<string[]>([])

  const visibleTables = tables.filter(table => !hidden.includes(table.id))

  const initialNodes: RFNode[] = tables
    .filter(table => !hidden.includes(table.id))
    .map(table => ({
      id: table.id,
      data: {
        id: table.id,
        name: table.name,
        label: table.display_name,
        metadata: table.metadata,
        columns: table.columns,
        sourceTables: table.sourceTables,
        hiddenSourceTables: table.sourceTables
          .filter(t => hidden.includes(t.id))
          .map(t => t.id),
        destinationTables: table.destinationTables,
        hiddenDestinationTables: table.destinationTables
          .filter(t => hidden.includes(t.id))
          .map(t => t.id),
        expanded: expanded.includes(table.id),
        onExpand(value: boolean) {
          setExpanded(
            value
              ? expanded.concat(table.id)
              : expanded.filter(e => e !== table.id)
          )
        },
        onShow(values: string[]) {
          setHidden([...hidden.filter(a => !values.includes(a))])
        },
      },
      position,
    }))

  const nameToNode = (name: string) => tables.find(n => n.name === name)

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
      const sourceTable = visibleTables.find(table =>
        table.columns.some(column => column.id === edge.source)
      )
      if (!sourceTable) return null

      const destinationTable = visibleTables.find(table =>
        table.columns.some(column => column.id === edge.target)
      )
      if (!destinationTable) return null

      if (sourceTable.id === destinationTable.id) return null

      const sourceHandle = expanded.includes(sourceTable.id)
        ? sourceTable.columns.find(c => c.id === edge.source)?.name
        : null
      const targetHandle = expanded.includes(destinationTable.id)
        ? destinationTable.columns.find(c => c.id === edge.target)?.name
        : null

      return {
        ...edge,
        source: sourceTable.id,
        sourceHandle,
        target: destinationTable.id,
        targetHandle,
      }
    })
    .filter(notEmpty)

  return (
    <BaseGraph
      initialNodes={filteredNodes}
      initialEdges={transformedEdges}
      expanded={expanded}
    />
  )
}

export default Graph
