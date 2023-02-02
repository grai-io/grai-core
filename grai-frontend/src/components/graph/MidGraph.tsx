import React, { useState } from "react"
import BaseGraph from "./BaseGraph"
import { Edge as RFEdge, Node as RFNode } from "reactflow"
import notEmpty from "helpers/notEmpty"
import { Edge, EnhancedTable } from "helpers/graph"
import { ErrorData } from "./ErrorEdge"
import { BaseNodeData } from "./BaseNode"

export interface GraiNodeMetadata {
  node_type?: "Table" | "Column" | null
  table_name?: string | null
}

export interface Error {
  sourceId: string | undefined
  destinationId: string | undefined
  source: string
  destination: string
  test: string
  message: string
}

export interface Column {
  id: string
  name: string
}

export interface Table extends EnhancedTable {
  id: string
  name: string
  display_name: string
  data_source: string
  columns: Column[]
  metadata: {
    grai?: GraiNodeMetadata | null
  } | null
}

type GraphProps = {
  tables: Table[]
  edges: Edge[]
  errors?: Error[] | null
  initialHidden?: string[]
}

const position = { x: 0, y: 0 }

const MidGraph: React.FC<GraphProps> = ({
  tables,
  edges,
  errors,
  initialHidden,
}) => {
  const [hidden, setHidden] = useState<string[]>(initialHidden ?? [])
  const [expanded, setExpanded] = useState<string[]>([])

  const visibleTables = tables.filter(table => !hidden.includes(table.id))

  const initialTables: RFNode<BaseNodeData>[] = tables
    .filter(table => !hidden.includes(table.id))
    .map(table => ({
      id: table.id,
      data: {
        id: table.id,
        name: table.name,
        label: table.display_name,
        data_source: table.data_source,
        metadata: table.metadata,
        columns: table.columns,
        source_tables: table.source_tables,
        hiddenSourceTables: table.source_tables
          .filter(t => hidden.includes(t.id))
          .map(t => t.id),
        destination_tables: table.destination_tables,
        hiddenDestinationTables: table.destination_tables
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
        highlight: false,
      },
      position,
    }))

  const initialEdges: RFEdge<ErrorData>[] = edges.map(edge => {
    const edgeErrors = errors?.filter(
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
      data: {
        errors: edgeErrors,
      },
      type: edgeErrors && edgeErrors.length > 0 ? "error" : undefined,
      labelStyle: { fill: "red", fontWeight: 700 },
      zIndex: 10,
    }
  })

  const transformedEdges = initialEdges
    .map(edge => {
      const sourceTable = visibleTables.find(
        table =>
          table.id === edge.source ||
          table.columns.some(column => column.id === edge.source)
      )
      if (!sourceTable) return null

      const destinationTable = visibleTables.find(
        table =>
          table.id === edge.target ||
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
      initialNodes={initialTables}
      initialEdges={transformedEdges}
      expanded={expanded}
    />
  )
}

export default MidGraph
