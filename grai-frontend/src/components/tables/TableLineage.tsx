import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesTableLineage,
  GetTablesAndEdgesTableLineageVariables,
} from "./__generated__/GetTablesAndEdgesTableLineage"
import Graph2 from "components/graph/Graph2"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesTableLineage(
    $organisationName: String!
    $workspaceName: String!
    $tableId: ID!
    $n: Int!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(table_id: $tableId, n: $n) {
        id
        name
        namespace
        data_source
        columns {
          id
          name
          destinations
        }
        destinations
        all_destinations
        all_sources
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
  if (loading) return <Loading />

  const tables = data?.workspace.graph

  if (!tables || tables.length === 0) return <Alert>No tables found</Alert>

  return (
    <Box
      sx={{
        height: "calc(100vh - 144px)",
      }}
      data-testid="table-lineage"
    >
      <Graph2
        tables={tables}
        errors={false}
        // initialHidden={hiddenTables}
        controlOptions={{
          steps: {
            value,
            setValue,
          },
        }}
      />
    </Box>
  )
}

export default TableLineage
