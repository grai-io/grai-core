import notEmpty from "./notEmpty"

export interface GraiNodeMetadata {
  node_type?: "Table" | "Column" | null
  table_name?: string | null
}

export interface Node {
  id: string
  name: string
  display_name: string
  metadata: {
    node_type?: string | null
    grai?: GraiNodeMetadata | null
  } | null
}

export interface GraiEdgeMetadata {
  edge_type?: "TableToColumn" | "Edge" | null
}

export interface Edge {
  id: string
  source: {
    id: string
  }
  destination: {
    id: string
  }
  metadata: {
    constraint_type?: string | null
    grai?: GraiEdgeMetadata | null
    "grai-source-dbt"?: {
      constraint_type?: string | null
    } | null
  } | null
}

type BaseTable<N extends Node> = N & {
  columns: N[]
}

export type Table<N extends Node> = N &
  BaseTable<N> & {
    sourceTables: BaseTable<N>[]
    destinationTables: BaseTable<N>[]
  }

export const nodeIsTable = (node: Node) => true
// node.metadata?.grai?.node_type === "Table" ||
// node.metadata?.node_type === "Table" ||
// node.metadata?.node_type === "BASE TABLE"

//edge.metadata?.grai?.edge_type === "Edge" ||

const tableColumns = <N extends Node>(table: N, nodes: N[], edges: Edge[]) =>
  edges
    .filter(
      edge =>
        edge.source.id === table.id &&
        edge.metadata?.["grai-source-dbt"]?.constraint_type === "belongs_to2"
    )
    .map(edge => nodes.find(node => node.id === edge.destination.id))
    .filter(notEmpty)

const nodesToBaseTables = <N extends Node>(
  nodes: N[],
  edges: Edge[]
): BaseTable<N>[] =>
  nodes.filter(nodeIsTable).map(table => ({
    ...table,
    columns: tableColumns(table, nodes, edges),
  }))

const nodeToBaseTable = <N extends Node>(
  node: N,
  nodes: N[],
  edges: Edge[]
): BaseTable<N> => ({
  ...node,
  columns: tableColumns(node, nodes, edges),
})

const tableOrColumnsMatch = <N extends Node>(table: BaseTable<N>, id: string) =>
  table.id === id || table.columns.some(c => c.id === id)

export const nodesToTables = <N extends Node>(
  nodes: N[],
  edges: Edge[]
): Table<N>[] => {
  const tables = nodesToBaseTables(nodes, edges)

  return tables.map(table => {
    const sourceTables = tables.filter(t =>
      edges.some(
        e =>
          tableOrColumnsMatch(table, e.source.id) &&
          tableOrColumnsMatch(t, e.destination.id)
      )
    )
    const destinationTables = tables.filter(t =>
      edges.some(
        e =>
          tableOrColumnsMatch(table, e.destination.id) &&
          tableOrColumnsMatch(t, e.source.id)
      )
    )

    return { ...table, sourceTables, destinationTables }
  })
}

export const nodeToTable = <N extends Node>(
  node: N,
  nodes: N[],
  edges: Edge[]
) => {
  const table = nodeToBaseTable(node, nodes, edges)
  const tables = nodesToBaseTables(nodes, edges)

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
}
