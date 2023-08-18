import React, { useState } from "react"
import { gql, useLazyQuery } from "@apollo/client"
import { Edge as RFEdge, Node as RFNode, Viewport } from "reactflow"
import notEmpty from "helpers/notEmpty"
import useWorkspace from "helpers/useWorkspace"
import {
  GetGraphLoadTable,
  GetGraphLoadTableVariables,
} from "./__generated__/GetGraphLoadTable"
import BaseGraph from "./BaseGraph"
import { BaseNodeData } from "./BaseNode"
import { ControlOptions } from "./controls/GraphControls"
import { Filter } from "components/filters/filters"

export const GET_GRAPH_LOAD_TABLE = gql`
  query GetGraphLoadTable(
    $organisationName: String!
    $workspaceName: String!
    $tableId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(filters: { table_id: $tableId, n: 0 }) {
        id
        name
        display_name
        namespace
        x
        y
        data_source
        columns {
          id
          name
          display_name
          destinations
        }
        destinations
        table_destinations
        table_sources
      }
    }
  }
`

export interface ResultError {
  source: string
  destination: string
  test: string
  message: string
  test_pass: boolean
}

interface NodeWithName {
  id: string
  name: string
}
interface Column extends NodeWithName {
  display_name: string
  sources?: string[]
  destinations: string[]
}

export interface Table extends NodeWithName {
  display_name: string
  x: number
  y: number
  data_source: string | null
  columns: Column[]
  sources?: string[]
  destinations: string[]
  table_destinations?: string[] | null
  table_sources?: string[] | null
}

type GraphComponentProps = {
  tables: Table[]
  errors?: ResultError[] | null
  loading?: boolean
  limitGraph?: boolean
  controlOptions?: ControlOptions
  throwMissingTable?: boolean
  alwaysShow?: boolean
  fitView?: boolean
  onMove?: (viewport: Viewport) => void
  onRefresh?: () => void
  refreshLoading?: boolean
  filters: string[]
  setFilters: (filters: string[]) => void
  inlineFilters: Filter[]
  setInlineFilters: (filters: Filter[]) => void
  defaultViewport?: Viewport
}

const GraphComponent: React.FC<GraphComponentProps> = ({
  tables,
  errors,
  loading,
  limitGraph,
  controlOptions,
  throwMissingTable,
  alwaysShow,
  fitView,
  onMove,
  onRefresh,
  refreshLoading,
  filters,
  setFilters,
  inlineFilters,
  setInlineFilters,
  defaultViewport,
}) => {
  const { organisationName, workspaceName } = useWorkspace()

  const [loadedTables, setLoadedTables] = useState<Table[]>([])
  const [expanded, setExpanded] = useState<string[]>([])
  const [search, setSearch] = useState<string | null>(null)

  const [loadTable] = useLazyQuery<
    GetGraphLoadTable,
    GetGraphLoadTableVariables
  >(GET_GRAPH_LOAD_TABLE)

  const handleLoadTable = async (tables: string[]) => {
    //TODO: Switch to multi table query with manual cache checking
    const results = await Promise.all(
      tables.map(tableId =>
        loadTable({
          variables: {
            organisationName,
            workspaceName,
            tableId,
          },
        }).then(res => res.data?.workspace.graph[0]),
      ),
    )

    setLoadedTables([...loadedTables, ...results.filter(notEmpty)])
  }

  const columns: NodeWithName[] = errors
    ? tables.reduce<NodeWithName[]>(
        (res, table) => res.concat(table.columns),
        [],
      )
    : []

  const tablesAndColumns = columns.concat(tables)

  const nameToNode = (name: string) =>
    tablesAndColumns.find(n => n.name.toLowerCase() === name.toLowerCase())

  const enrichedErrors = errors?.map(error => ({
    ...error,
    sourceId: nameToNode(error.source)?.id,
    destinationId: nameToNode(error.destination)?.id,
  }))

  const allTables = tables.concat(loadedTables)

  const initialTables: RFNode<BaseNodeData>[] = allTables.map(table => {
    const searchMatch = search
      ? table.name.toLowerCase().includes(search.toLowerCase())
      : false

    return {
      id: table.id,
      data: {
        id: table.id,
        name: table.name,
        label: table.display_name,
        data_source: table.data_source,
        columns: table.columns,
        hiddenSourceTables: (table.table_destinations ?? []).filter(
          t => !allTables.map(t => t.id).includes(t),
        ),
        hiddenDestinationTables: (table.table_sources ?? []).filter(
          t => !allTables.map(t => t.id).includes(t),
        ),
        expanded: expanded.includes(table.id),
        onExpand(value: boolean) {
          setExpanded(
            value
              ? expanded.concat(table.id)
              : expanded.filter(e => e !== table.id),
          )
        },
        onShow: handleLoadTable,
        highlight: false,
        searchHighlight: searchMatch,
        searchDim: search ? !searchMatch : false,
        alwaysShow,
      },
      position: {
        x: table.x,
        y: table.y,
      },
    }
  })

  const getTableFromColumnId = (id: string) => {
    const table = allTables.find(table =>
      table.columns.some(col => col.id === id),
    )

    if (!table && throwMissingTable) throw new Error(`Table not found ${id}`)

    return table
  }

  const generateEdge = (
    source: string,
    sourceHandle: string,
    target: string,
    targetHandle: string,
    tests: ResultError[] = [],
  ) => ({
    id: `${source}-${sourceHandle}-${target}-${targetHandle}`,
    source,
    sourceHandle,
    target,
    targetHandle,
    data: { tests },
    type: "test",
    labelStyle: { fill: "red", fontWeight: 700 },
    zIndex: 10,
  })

  const edges = allTables.reduce<RFEdge[]>((res, table) => {
    const tableExpanded = expanded.includes(table.id)

    if (!tableExpanded) {
      const otherColumnIds = table.columns.reduce<Set<string>>(
        (res, column) => {
          const columnEdges = column.destinations.reduce<Set<string>>(
            (tableRes, destination) => tableRes.add(destination),
            new Set(),
          )
          Array.from(columnEdges).forEach(id => res.add(id))

          return res
        },
        new Set(),
      )

      const destinationEdges = Array.from(otherColumnIds).reduce<{
        tables: Set<Table>
        edges: RFEdge[]
      }>(
        (res, destinationId) => {
          const destinationTable = getTableFromColumnId(destinationId)

          if (!destinationTable) return res

          const destinationExpanded = expanded.includes(destinationTable.id)

          destinationExpanded
            ? res.edges.push(
                generateEdge(
                  table.id,
                  "all",
                  destinationTable.id,
                  destinationId,
                  enrichedErrors?.filter(
                    error =>
                      table.columns.some(col => error.sourceId === col.id) &&
                      error.destinationId === destinationId,
                  ),
                ),
              )
            : res.tables.add(destinationTable)

          return res
        },
        { tables: new Set(), edges: [] },
      )

      table.destinations
        .map(destinationId => allTables.find(t => t.id === destinationId))
        .filter(notEmpty)
        .forEach(destination => destinationEdges.tables.add(destination))

      const edges = destinationEdges.edges.concat(
        Array.from(destinationEdges.tables).map(destinationTable =>
          generateEdge(
            table.id,
            "all",
            destinationTable.id,
            "all",
            enrichedErrors?.filter(
              error =>
                table.columns.some(col => error.sourceId === col.id) &&
                destinationTable.columns.some(
                  col => error.destinationId === col.id,
                ),
            ),
          ),
        ),
      )

      return res.concat(edges)
    }

    return res
      .concat(
        table.columns.reduce<RFEdge[]>(
          (tableRes, column) =>
            tableRes.concat(
              column.destinations.reduce<RFEdge[]>((res, destination) => {
                const destinationTable = getTableFromColumnId(destination)

                if (!destinationTable) return res

                const destinationExpanded = expanded.includes(
                  destinationTable.id,
                )

                return res.concat(
                  generateEdge(
                    table.id,
                    column.id,
                    destinationTable.id,
                    destinationExpanded ? destination : "all",
                    enrichedErrors?.filter(
                      error =>
                        error.sourceId === column.id &&
                        error.destinationId === destination,
                    ),
                  ),
                )
              }, []),
            ),
          [],
        ),
      )
      .concat(
        table.destinations
          .filter(destination => allTables.map(t => t.id).includes(destination))
          .map(destination =>
            generateEdge(
              table.id,
              "all",
              destination,
              "all",
              enrichedErrors?.filter(
                error =>
                  error.sourceId === table.id &&
                  error.destinationId === destination,
              ),
            ),
          )
          .filter(notEmpty),
      )
  }, [])

  return (
    <BaseGraph
      initialNodes={initialTables}
      initialEdges={edges}
      expanded={expanded}
      errors={false}
      // errors={!!errors}
      search={search}
      onSearch={setSearch}
      loading={loading}
      controlOptions={controlOptions}
      fitView={fitView}
      onMove={onMove}
      onRefresh={onRefresh}
      refreshLoading={refreshLoading}
      filters={filters}
      setFilters={setFilters}
      inlineFilters={inlineFilters}
      setInlineFilters={setInlineFilters}
      defaultViewport={defaultViewport}
    />
  )
}

export default GraphComponent
