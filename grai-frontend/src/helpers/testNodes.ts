export const sourceTable = {
  id: "1",
  namespace: "default",
  name: "N1",
  display_name: "N1",
  data_source: "test",
  x: 0,
  y: 0,
  columns: [
    {
      id: "c1",
      name: "N3",
      display_name: "N3 Node",
      destinations: ["c2"],
    },
  ],
  destinations: [],
  table_destinations: ["2"],
  table_sources: [],
}

export const destinationTable = {
  id: "2",
  namespace: "default",
  name: "N2 Node",
  display_name: "N2 Node",
  data_source: "test",
  x: 0,
  y: 0,
  columns: [
    {
      id: "c2",
      name: "C2 Column",
      display_name: "C2 Column",
      destinations: [],
    },
  ],
  destinations: [],
  table_destinations: [],
  table_sources: ["1"],
}

export const spareTable = {
  id: "3",
  namespace: "default",
  name: "N3",
  display_name: "N3",
  data_source: "test",
  x: 0,
  y: 0,
  columns: [],
  destinations: [],
  table_destinations: [],
  table_sources: [],
}
