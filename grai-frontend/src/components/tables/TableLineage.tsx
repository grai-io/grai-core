import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import GraphComponent from "components/graph/GraphComponent"
import useCombinedFilters from "components/graph/useCombinedFilters"
import useFilters from "components/graph/useFilters"
import useInlineFilters from "components/graph/useInlineFilters"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesTableLineage,
  GetTablesAndEdgesTableLineageVariables,
} from "./__generated__/GetTablesAndEdgesTableLineage"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesTableLineage(
    $organisationName: String!
    $workspaceName: String!
    $tableId: ID!
    $n: Int!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(filters: { table_id: $tableId, n: $n }) {
        id
        name
        display_name
        namespace
        x
        y
        data_source
        columns {
          id
          name
          display_name
          destinations {
            edge_id
            column_id
          }
        }
        destinations {
          edge_id
          table_id
        }
        table_destinations
        table_sources
      }
    }
  }
`

interface Table {
  id: string
  display_name: string
}

type TableLineageProps = {
  table: Table
}

const TableLineage: React.FC<TableLineageProps> = ({ table }) => {
  const [value, setValue] = useState(1)
  const { organisationName, workspaceName } = useWorkspace()
  const { combinedFilters } = useCombinedFilters(
    `tables-${table.id}-graph-filters`,
    `tables-${table.id}-graph-inline-filters`,
  )

  const { loading, error, data } = useQuery<
    GetTablesAndEdgesTableLineage,
    GetTablesAndEdgesTableLineageVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
      tableId: table.id,
      n: value,
    },
  })

  if (error) return <GraphError error={error} />

  const tables = data?.workspace.graph

  if (!loading && (!tables || tables.length === 0))
    return <Alert>No tables found</Alert>

  return (
    <Box
      sx={{
        height: "calc(100vh - 144px)",
      }}
      data-testid="table-lineage"
    >
      <GraphComponent
        tables={tables ?? []}
        loading={loading}
        fitView
        controlOptions={{
          steps: {
            value,
            setValue,
          },
        }}
        combinedFilters={combinedFilters}
      />
    </Box>
  )
}

export default TableLineage
