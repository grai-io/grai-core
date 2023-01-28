export interface Column {
  id: string
}

export interface BaseTable {
  id: string
  name: string
  display_name: string
}

export interface Table extends BaseTable {
  columns: Column[]
}

export interface EnhancedTable extends BaseTable {
  sourceTables: Table[]
  destinationTables: Table[]
}

export interface Edge {
  id: string
  source: NodeID
  destination: NodeID
}

interface NodeID {
  id: string
}

const tableOrColumnsMatch = (table: Table, id: string) =>
  table.id === id || table.columns.some(c => c.id === id)

export const tableToEnhancedTable = <T extends Table>(
  table: T,
  tables: T[],
  edges: Edge[]
): EnhancedTable & T => {
  const sourceTables = tables
    .filter(t => t.id !== table.id)
    .filter(t =>
      edges.some(
        e =>
          tableOrColumnsMatch(table, e.source.id) &&
          tableOrColumnsMatch(t, e.destination.id)
      )
    )
  const destinationTables = tables
    .filter(t => t.id !== table.id)
    .filter(t =>
      edges.some(
        e =>
          tableOrColumnsMatch(table, e.destination.id) &&
          tableOrColumnsMatch(t, e.source.id)
      )
    )

  return { ...table, sourceTables, destinationTables }
}

export const tablesToEnhancedTables = <T extends Table>(
  tables: T[],
  edges: Edge[]
): (EnhancedTable & T)[] =>
  tables.map(table => tableToEnhancedTable<T>(table, tables, edges))
