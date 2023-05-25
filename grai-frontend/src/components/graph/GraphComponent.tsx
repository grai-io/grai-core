import React, { useState } from "react"
import { gql, useLazyQuery } from "@apollo/client"
import { Edge as RFEdge, Node as RFNode } from "reactflow"
import notEmpty from "helpers/notEmpty"
import useWorkspace from "helpers/useWorkspace"
import {
  GetGraphLoadTable,
  GetGraphLoadTableVariables,
} from "./__generated__/GetGraphLoadTable"
import BaseGraph from "./BaseGraph"
import { BaseNodeData } from "./BaseNode"
import { ControlOptions } from "./controls/GraphControls"

export const GET_GRAPH_LOAD_TABLE = gql`
  query GetGraphLoadTable(
    $organisationName: String!
    $workspaceName: String!
    $tableId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(table_id: $tableId, n: 0) {
        id
        name
        namespace
        data_source
        columns {
          id
          name
          destinations
        }
        destinations
        all_destinations
        all_sources
      }
    }
  }
`

const position = { x: 0, y: 0 }

export interface Error {
  source: string
  destination: string
  test: string
  message: string
  test_pass: boolean
}

interface Column {
  id: string
  name: string
  sources?: string[]
  destinations: string[]
}

export interface Table {
  id: string
  name: string
  data_source: string
  columns: Column[]
  sources?: string[]
  destinations: string[]
  all_destinations?: string[] | null
  all_sources?: string[] | null
}

type GraphComponentProps = {
  tables: Table[]
  errors: any
  loading?: boolean
  limitGraph?: boolean
  controlOptions?: ControlOptions
  throwMissingTable?: boolean
}

const GraphComponent: React.FC<GraphComponentProps> = ({
  tables,
  errors,
  loading,
  limitGraph,
  controlOptions,
  throwMissingTable,
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
        }).then(res => res.data?.workspace.graph[0])
      )
    )

    setLoadedTables([...loadedTables, ...results.filter(notEmpty)])
  }

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
        label: table.name,
        data_source: table.data_source,
        columns: table.columns,
        hiddenSourceTables: (table.all_destinations ?? []).filter(
          t => !allTables.map(t => t.id).includes(t)
        ),
        hiddenDestinationTables: (table.all_sources ?? []).filter(
          t => !allTables.map(t => t.id).includes(t)
        ),
        expanded: expanded.includes(table.id),
        onExpand(value: boolean) {
          setExpanded(
            value
              ? expanded.concat(table.id)
              : expanded.filter(e => e !== table.id)
          )
        },
        onShow: handleLoadTable,
        highlight: false,
        searchHighlight: searchMatch,
        searchDim: search ? !searchMatch : false,
      },
      position,
    }
  })

  const getTable = (id: string) => {
    const table = allTables.find(table =>
      table.columns.some(col => col.id === id)
    )

    if (!table && throwMissingTable) throw new Error(`Table not found ${id}`)

    return table
  }

  const generateEdge = (
    source: string,
    sourceHandle: string,
    target: string,
    targetHandle: string
  ) => ({
    id: `${source}-${target}`,
    source,
    sourceHandle,
    target,
    targetHandle,
    // data: {
    //   tests: edgeTests,
    // },
    type: "test",
    labelStyle: { fill: "red", fontWeight: 700 },
    zIndex: 10,
  })

  const edges = allTables.reduce<RFEdge[]>((res, table) => {
    const tableExpanded = expanded.includes(table.id)

    if (!tableExpanded) {
      // List of either column Ids or tableIds depending on whether the other table is expanded
      const otherColumnIds = table.columns.reduce<Set<string>>(
        (res, column) => {
          const columnEdges = column.destinations.reduce<Set<string>>(
            (tableRes, destination) => tableRes.add(destination),
            new Set()
          )
          Array.from(columnEdges).forEach(id => res.add(id))

          return res
        },
        new Set()
      )

      const destinationEdges = Array.from(otherColumnIds).reduce<{
        tables: Set<string>
        edges: RFEdge[]
      }>(
        (res, destinationId) => {
          const destinationTable = getTable(destinationId)

          if (!destinationTable) return res

          const destinationExpanded = expanded.includes(destinationTable.id)

          destinationExpanded
            ? res.edges.push(
                generateEdge(
                  table.id,
                  "all",
                  destinationTable.id,
                  destinationId
                )
              )
            : res.tables.add(destinationTable.id)

          return res
        },
        { tables: new Set(), edges: [] }
      )

      table.destinations
        .filter(destination => allTables.map(t => t.id).includes(destination))
        .forEach(destination => destinationEdges.tables.add(destination))

      const edges = destinationEdges.edges.concat(
        Array.from(destinationEdges.tables).map(destinationTableId =>
          generateEdge(table.id, "all", destinationTableId, "all")
        )
      )

      return res.concat(edges)
    }

    return res
      .concat(
        table.columns.reduce<RFEdge[]>(
          (tableRes, column) =>
            tableRes.concat(
              column.destinations.reduce<RFEdge[]>((res, destination) => {
                const destinationTable = getTable(destination)

                if (!destinationTable) return res

                const destinationExpanded = expanded.includes(
                  destinationTable.id
                )

                return res.concat(
                  generateEdge(
                    table.id,
                    column.id,
                    destinationTable.id,
                    destinationExpanded ? destination : "all"
                  )
                )
              }, [])
            ),
          []
        )
      )
      .concat(
        table.destinations
          .filter(destination => allTables.map(t => t.id).includes(destination))
          .map(destination => generateEdge(table.id, "all", destination, "all"))
          .filter(notEmpty)
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
    />
  )
}

export default GraphComponent
