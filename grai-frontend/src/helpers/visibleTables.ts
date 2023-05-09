interface Table {
  id: string
  source_tables: {
    data: {
      id: string
    }[]
  }
  destination_tables: {
    data: {
      id: string
    }[]
  }
}

const getHiddenTables = (
  tables: Table[],
  value: number,
  startTables: string[]
) => {
  const visibleTables: string[] = Array.from(Array(value).keys()).reduce(
    (res, value) =>
      res.concat(
        tables
          .filter(
            t =>
              t.source_tables.data.some(sourceTable =>
                res.includes(sourceTable.id)
              ) ||
              t.destination_tables.data.some(destinationTable =>
                res.includes(destinationTable.id)
              )
          )
          .map(t => t.id)
      ),
    startTables
  )

  return tables.filter(t => !visibleTables.includes(t.id))
}

export default getHiddenTables

interface Edge {
  source: {
    id: string
  }
  destination: {
    id: string
  }
}

interface TableWithColumns {
  id: string
  columns: {
    data: {
      id: string
    }[]
  }
}

export const getEdgeTables = (tables: TableWithColumns[], edge: Edge) =>
  tables.filter(
    t =>
      t.id === edge.source.id ||
      t.id === edge.destination.id ||
      t.columns.data.some(
        c => c.id === edge.source.id || c.id === edge.destination.id
      )
  )
