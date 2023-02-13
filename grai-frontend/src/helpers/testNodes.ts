export const columnNode = {
  id: "3",
  namespace: "default",
  name: "N3",
  display_name: "N3 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Column",
    },
  },
}

export const sourceTable = {
  id: "1",
  namespace: "default",
  name: "N1",
  display_name: "N1",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
  columns: [columnNode],
  source_tables: [],
  destination_tables: [],
}

export const destinationTable = {
  id: "2",
  namespace: "default",
  name: "N2",
  display_name: "N2 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
  columns: [],
  source_tables: [],
  destination_tables: [],
}

export const spareTable = {
  id: "3",
  namespace: "default",
  name: "N3",
  display_name: "N3 Node",
  is_active: true,
  data_source: "test",
  metadata: {
    grai: {
      node_type: "Table",
    },
  },
  columns: [],
  source_tables: [],
  destination_tables: [],
}
