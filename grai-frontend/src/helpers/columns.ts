interface GraiColumnMetadata {
  node_attributes: {
    data_type?: string | null
    is_nullable?: boolean | null
    is_primary_key?: boolean | null
    is_unique?: boolean | null
  }
}

export interface ColumnMetadata {
  grai: GraiColumnMetadata | null
}

interface RequirementEdge {
  metadata?: {
    grai?: {
      edge_attributes: {
        preserves_data_type?: boolean | null
        preserves_nullable?: boolean | null
        preserves_unique?: boolean | null
      }
    }
  } | null
  source: {
    id: string
    name: string
    display_name: string
    metadata: ColumnMetadata
  }
}

export interface Column {
  id: string
  name: string
  display_name: string
  metadata: ColumnMetadata | null
  requirements_edges: RequirementEdge[]
}

export interface EnrichedColumn extends Column {
  properties: string[]
  tests: Test[]
  requirements: Requirement[]
}

interface Source {
  name: string
  display_name: string
}

export type Test = {
  type: string
  text: string
  data_type?: string
  source: Source
  passed: boolean | null
}

type Requirement = {
  source: Source
  tests: Edge[]
}

export type Edge = Test & {
  preserved: boolean | null
}

export const columnTests = (column: Column, properties: string[]) =>
  column.requirements_edges.reduce<Test[]>((res, edge) => {
    const edge_attributes = edge.metadata?.grai?.edge_attributes
    const node_attributes = edge.source.metadata.grai?.node_attributes

    if (!edge_attributes || !node_attributes) return res

    //Nullable
    if (
      edge_attributes.preserves_nullable &&
      node_attributes.is_nullable === false
    )
      return res.concat({
        type: "not-null",
        text: "Not Null",
        source: edge.source,
        passed: properties.includes("Not Null"),
      })

    //Unique
    if (edge_attributes.preserves_unique && node_attributes.is_unique)
      return res.concat({
        type: "unique",
        text: "Unique",
        source: edge.source,
        passed: properties.includes("Unique"),
      })

    //Data type
    if (edge_attributes.preserves_data_type && node_attributes.data_type)
      return res.concat({
        type: "data-type",
        text: `Data Type: ${node_attributes.data_type}`,
        source: edge.source,
        data_type: node_attributes.data_type,
        passed:
          column.metadata?.grai?.node_attributes.data_type ===
          node_attributes.data_type,
      })

    return res
  }, [])

export const columnEdges = (column: Column, properties: string[]) =>
  column.requirements_edges.reduce<Edge[]>((res, edge) => {
    const edge_attributes = edge.metadata?.grai?.edge_attributes
    const node_attributes = edge.source.metadata.grai?.node_attributes

    if (!node_attributes) return res

    //Nullable
    if (node_attributes.is_nullable === false)
      return res.concat({
        type: "not-null",
        text: "Not Null",
        source: edge.source,
        passed: properties.includes("Not Null"),
        preserved: edge_attributes?.preserves_nullable ?? false,
      })

    //Unique
    if (node_attributes.is_unique)
      return res.concat({
        type: "unique",
        text: "Unique",
        source: edge.source,
        passed: properties.includes("Unique"),
        preserved: edge_attributes?.preserves_unique ?? false,
      })

    //Data type
    if (node_attributes.data_type)
      return res.concat({
        type: "data-type",
        text: `Data Type: ${node_attributes.data_type}`,
        source: edge.source,
        data_type: node_attributes.data_type,
        passed:
          column.metadata?.grai?.node_attributes.data_type ===
          node_attributes.data_type,
        preserved: edge_attributes?.preserves_data_type ?? false,
      })

    return res
  }, [])

export const columnProperties = (column: Column) => {
  const attributes = column.metadata?.grai?.node_attributes

  if (!attributes) return []

  const properties: string[] = []

  if (attributes.is_primary_key) properties.push("Primary Key")
  if (attributes.is_unique) properties.push("Unique")
  if (attributes.is_nullable === false) properties.push("Not Null")

  return properties
}

export const columnRequirements = (column: Column, properties: string[]) =>
  column.requirements_edges.map(edge => ({
    source: edge.source,
    tests: columnEdges(column, properties),
  }))

export const enrichColumn = (column: Column): EnrichedColumn => {
  const properties = columnProperties(column)
  const tests = columnTests(column, properties)
  const requirements = columnRequirements(column, properties)

  return { ...column, properties, tests, requirements }
}

export const enrichColumns = (columns: Column[]) => columns.map(enrichColumn)
