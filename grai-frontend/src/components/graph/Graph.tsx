import React from "react"
import { Edge } from "helpers/graph"
import notEmpty from "helpers/notEmpty"
import { ControlOptions } from "./controls/GraphControls"
import MidGraph, { Column, Table } from "./MidGraph"

export interface Error {
  source: string
  destination: string
  test: string
  message: string
  test_pass: boolean
}

type GraphProps = {
  tables: Table[]
  edges: Edge[]
  errors?: Error[] | null
  limitGraph?: boolean
  initialHidden?: string[]
  controlOptions?: ControlOptions
}

const Graph: React.FC<GraphProps> = ({
  tables,
  edges,
  errors,
  limitGraph,
  initialHidden,
  controlOptions,
}) => {
  const columns: Column[] = errors
    ? tables.reduce<Column[]>((res, table) => res.concat(table.columns), [])
    : []

  const tablesAndColumns = columns.concat(tables)

  const nameToNode = (name: string) =>
    tablesAndColumns.find(n => n.name.toLowerCase() === name.toLowerCase())

  const enrichedErrors = errors?.map(error => ({
    ...error,
    sourceId: nameToNode(error.source)?.id,
    destinationId: nameToNode(error.destination)?.id,
  }))

  const errorSourceIds =
    enrichedErrors?.map(error => error.sourceId).filter(notEmpty) ?? []

  const errorDestinationIds =
    enrichedErrors?.map(error => error.destinationId).filter(notEmpty) ?? []

  const errorTables = tables.filter(
    table =>
      errorSourceIds.includes(table.id) ||
      errorDestinationIds.includes(table.id) ||
      table.columns.filter(
        column =>
          errorSourceIds.includes(column.id) ||
          errorDestinationIds.includes(column.id)
      ).length > 0
  )

  const errorTableIds = errorTables.map(table => table.id)

  const initialHidden2 = limitGraph
    ? (initialHidden ?? []).concat(
        tables
          .filter(table => !errorTableIds.includes(table.id))
          .map(table => table.id)
      )
    : initialHidden ?? []

  return (
    <MidGraph
      tables={tables}
      edges={edges}
      errors={enrichedErrors}
      initialHidden={initialHidden2}
      controlOptions={controlOptions}
    />
  )
}

export default Graph
