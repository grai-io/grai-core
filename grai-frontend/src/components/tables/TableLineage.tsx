import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import React, { useState } from "react"
import theme from "theme"
import Loading from "components/layout/Loading"
import Graph from "components/graph/Graph"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesTableLineage,
  GetTablesAndEdgesTableLineageVariables,
} from "./__generated__/GetTablesAndEdgesTableLineage"
import useWorkspace from "helpers/useWorkspace"

const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesTableLineage(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
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
        source_tables {
          id
          name
          display_name
        }
        destination_tables {
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
  const [value, setValue] = useState(1)
  const { organisationName, workspaceName } = useWorkspace()
  const { loading, error, data } = useQuery<
    GetTablesAndEdgesTableLineage,
    GetTablesAndEdgesTableLineageVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const tables = data?.workspace.tables
  const edges = data?.workspace.other_edges ?? []

  if (!tables) return <Alert>No tables found</Alert>

  const visibleTables: string[] = [table.id]

  for (var i = 0; i < value; i++) {
    const tablesToAdd = tables.filter(
      t =>
        t.source_tables.some(sourceTable =>
          visibleTables.includes(sourceTable.id)
        ) ||
        t.destination_tables.some(destinationTable =>
          visibleTables.includes(destinationTable.id)
        )
    )

    visibleTables.push(...tablesToAdd.map(t => t.id))
  }

  const hiddenTables = tables.filter(t => !visibleTables.includes(t.id))

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
        tables={tables}
        edges={edges}
        initialHidden={hiddenTables.map(n => n.id)}
        controlOptions={{
          n: {
            value,
            setValue,
          },
        }}
      />
    </Box>
  )
}

export default TableLineage
