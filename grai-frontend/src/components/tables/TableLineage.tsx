import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import React from "react"
import theme from "theme"
import Loading from "components/layout/Loading"
import { useParams } from "react-router-dom"
import Graph from "components/graph/Graph"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesTableLineage,
  GetTablesAndEdgesTableLineageVariables,
} from "./__generated__/GetTablesAndEdgesTableLineage"
import { tablesToEnhancedTables } from "helpers/graph2"

const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesTableLineage($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      tables {
        id
        namespace
        name
        display_name
        data_source
        metadata
        columns {
          id
          name
          display_name
        }
      }
      other_edges {
        id
        source {
          id
        }
        destination {
          id
        }
        metadata
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
  const { workspaceId } = useParams()
  const { loading, error, data } = useQuery<
    GetTablesAndEdgesTableLineage,
    GetTablesAndEdgesTableLineageVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const tables = data?.workspace.tables
  const edges = data?.workspace.other_edges ?? []

  if (!tables) return <Alert>No tables found</Alert>

  const enhancedTables = tablesToEnhancedTables(data.workspace.tables, edges)

  const hiddenTables = enhancedTables.filter(t => {
    if (t.id === table.id) return false

    return !(
      t.sourceTables.some(sourceTable => sourceTable.id === table.id) ||
      t.destinationTables.some(sourceTable => sourceTable.id === table.id)
    )
  })

  return (
    <Box
      sx={{
        height: "calc(100vh - 226px)",
        width: "100%",
        backgroundColor: theme.palette.grey[100],
        mt: 2,
      }}
    >
      <Graph
        tables={enhancedTables}
        edges={edges}
        initialHidden={hiddenTables.map(n => n.id)}
      />
    </Box>
  )
}

export default TableLineage
