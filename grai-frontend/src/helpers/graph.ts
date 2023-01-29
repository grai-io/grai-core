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
  source_tables: BaseTable[]
  destination_tables: BaseTable[]
}

export interface Edge {
  id: string
  source: NodeID
  destination: NodeID
}

interface NodeID {
  id: string
}
