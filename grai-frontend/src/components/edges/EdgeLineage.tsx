import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import {
  GetTablesAndEdges,
  GetTablesAndEdgesVariables,
} from "pages/__generated__/GetTablesAndEdges"
import useWorkspace from "helpers/useWorkspace"
import getHiddenTables, { getEdgeTables } from "helpers/visibleTables"
import Graph from "components/graph/Graph"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesEdgeLineage(
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

interface Node {
  id: string
}

interface Edge {
  id: string
  source: Node
  destination: Node
}

type EdgeLineageProps = {
  edge: Edge
}

const EdgeLineage: React.FC<EdgeLineageProps> = ({ edge }) => {
  const [value, setValue] = useState(1)
  const { organisationName, workspaceName } = useWorkspace()
  const { loading, error, data } = useQuery<
    GetTablesAndEdges,
    GetTablesAndEdgesVariables
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

  const startTables = getEdgeTables(tables, edge).map(t => t.id)

  const hiddenTables = getHiddenTables(tables, value - 1, startTables).map(
    n => n.id
  )

  return (
    <Box
      sx={{
        height: "calc(100vh - 144px)",
      }}
      data-testid="edge-lineage"
    >
      <Graph
        tables={tables}
        edges={edges}
        initialHidden={hiddenTables}
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

export default EdgeLineage
