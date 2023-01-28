import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import React from "react"
import theme from "theme"
import Loading from "components/layout/Loading"
// import { Table as TableType } from "helpers/graph"
import { useParams } from "react-router-dom"
import Graph from "components/graph/Graph"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesTableLineage,
  GetTablesAndEdgesTableLineageVariables,
} from "./__generated__/GetTablesAndEdgesTableLineage"

const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesTableLineage($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      tables {
        id
        namespace
        name
        display_name
        is_active
        data_source
        metadata
      }
      edges {
        id
        is_active
        data_source
        source {
          id
          namespace
          name
          display_name
          data_source
          is_active
          metadata
        }
        destination {
          id
          namespace
          name
          display_name
          data_source
          is_active
          metadata
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

  if (!data?.workspace.tables || !data.workspace.edges) return null

  const hiddenTables = data?.workspace.tables.filter(t => {
    if (t.id === table.id) return false

    return true

    // return !(
    //   t.sourceTables.some(sourceTable => sourceTable.id === table.id) ||
    //   t.destinationTables.some(sourceTable => sourceTable.id === table.id)
    // )
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
      {/* <Graph
        tables={tables}
        tables={data.workspace.tables}
        edges={data.workspace.edges}
        initialHidden={hiddenTables.map(n => n.id)}
      /> */}
    </Box>
  )
}

export default TableLineage
