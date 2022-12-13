export interface Node {
  id: string
  name: string
  displayName: string
  metadata: {
    node_type: string
    table_name?: string
  }
}

interface Edge {
  id: string
  source: {
    id: string
  }
  destination: {
    id: string
  }
}

type BaseTable<N extends Node> = N & {
  columns: N[]
}

export type Table<N extends Node> = N &
  BaseTable<N> & {
    sourceTables: BaseTable<N>[]
    destinationTables: BaseTable<N>[]
  }

const nodeIsTable = (node: Node) => node.metadata.node_type === "Table"

const sameTable = (table: Node, column: Node) =>
  table.metadata.table_name === column.metadata.table_name ||
  table.name === `public.${column.metadata.table_name}`

const nodesToBaseTables = <N extends Node>(nodes: N[]): BaseTable<N>[] => {
  const tables = nodes.filter(nodeIsTable)
  const columns = nodes.filter(n => !nodeIsTable(n))

  const tablesWithColumns = tables.map(table => {
    const tableColumns = columns.filter(column => sameTable(table, column))

    return {
      ...table,
      columns: tableColumns,
    }
  })

  return tablesWithColumns
}

export const nodesToTables = <N extends Node>(
  nodes: N[],
  edges: Edge[]
): Table<N>[] => {
  const tables = nodesToBaseTables(nodes)

  return tables.map(table => {
    const sourceTables = tables.filter(t =>
      edges.some(
        e =>
          table.columns.some(c => c.id === e.source.id) &&
          t.columns.some(c => c.id === e.destination.id)
      )
    )
    const destinationTables = tables.filter(t =>
      edges.some(
        e =>
          table.columns.some(c => c.id === e.destination.id) &&
          t.columns.some(c => c.id === e.source.id)
      )
    )

    return { ...table, sourceTables, destinationTables }
  })
}
