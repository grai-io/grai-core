import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import theme from "theme"
import Graph from "components/graph/Graph"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesTableLineage,
  GetTablesAndEdgesTableLineageVariables,
} from "./__generated__/GetTablesAndEdgesTableLineage"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesTableLineage(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      tables {
        data {
          id
          namespace
          name
          display_name
          data_source
          metadata
          columns {
            data {
              id
              name
              display_name
            }
          }
          source_tables {
            data {
              id
              name
              display_name
            }
          }
          destination_tables {
            data {
              id
              name
              display_name
            }
          }
        }
      }
      other_edges {
        data {
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

  const tables = data?.workspace.tables.data

  if (!tables || tables.length === 0) return <Alert>No tables found</Alert>

  const edges = data.workspace.other_edges.data

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
    [table.id]
  )

  const hiddenTables = tables.filter(t => !visibleTables.includes(t.id))

  return (
    <Box
      sx={{
        height: "calc(100vh - 160px)",
        width: "100%",
        backgroundColor: theme.palette.grey[100],
        mt: 2,
      }}
      data-testid="table-lineage"
    >
      <Graph
        tables={tables}
        edges={edges}
        initialHidden={hiddenTables.map(n => n.id)}
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
