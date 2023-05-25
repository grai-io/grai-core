export const sourceTable = {
  id: "1",
  namespace: "default",
  name: "N1",
  data_source: "test",
  columns: [
    {
      id: "c1",
      name: "N3 Node",
      destinations: ["c2"],
    },
  ],
  destinations: [],
  all_destinations: ["2"],
  all_sources: [],
}

export const destinationTable = {
  id: "2",
  namespace: "default",
  name: "N2 Node",
  data_source: "test",
  columns: [
    {
      id: "c2",
      name: "C2 Column",
      destinations: [],
    },
  ],
  destinations: [],
  all_destinations: [],
  all_sources: ["1"],
}

export const spareTable = {
  id: "3",
  namespace: "default",
  name: "N3",
  data_source: "test",
  columns: [],
  destinations: [],
  all_destinations: [],
  all_sources: [],
}
