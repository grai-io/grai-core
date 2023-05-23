import React, { useState } from "react"
import { Edge as RFEdge, Node as RFNode } from "reactflow"
import notEmpty from "helpers/notEmpty"
import BaseGraph from "./BaseGraph"
import { BaseNodeData } from "./BaseNode"

const position = { x: 0, y: 0 }

interface Column {
  id: string
  name: string
  sources?: string[]
  destinations: string[]
}

interface Table {
  id: string
  name: string
  data_source: string
  columns: Column[]
  sources?: string[]
  destinations: string[]
}

type Graph2Props = {
  tables: Table[]
  errors: any
  loading?: boolean
  limitGraph?: boolean
}

const Graph2: React.FC<Graph2Props> = ({
  tables,
  errors,
  loading,
  limitGraph,
}) => {
  const [hidden, setHidden] = useState<string[]>([])
  const [expanded, setExpanded] = useState<string[]>([])
  const [search, setSearch] = useState<string | null>(null)

  const initialTables: RFNode<BaseNodeData>[] = tables
    .filter(table => !hidden.includes(table.id))
    .map(table => {
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
          source_tables: table.sources,
          hiddenSourceTables: (table.sources ?? []).filter(t =>
            hidden.includes(t)
          ),
          destination_tables: table.destinations,
          hiddenDestinationTables: table.destinations.filter(t =>
            hidden.includes(t)
          ),

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
          searchHighlight: searchMatch,
          searchDim: search ? !searchMatch : false,
        },
        position,
      }
    })

  const getTable = (id: string) => {
    const table = tables.find(table => table.columns.some(col => col.id === id))

    if (!table) throw new Error(`Table not found ${id}`)

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

  const edges = tables.reduce<RFEdge[]>((res, table) => {
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

      table.destinations.forEach(destination =>
        destinationEdges.tables.add(destination)
      )

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
          .map(destination => {
            const destinationTable = getTable(destination)

            return generateEdge(table.id, "all", destinationTable.id, "all")
          })
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
    />
  )
}

export default Graph2
