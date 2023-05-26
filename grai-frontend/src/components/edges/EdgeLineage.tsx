import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import GraphComponent from "components/graph/GraphComponent"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesEdgeLineage,
  GetTablesAndEdgesEdgeLineageVariables,
} from "./__generated__/GetTablesAndEdgesEdgeLineage"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesEdgeLineage(
    $organisationName: String!
    $workspaceName: String!
    $edgeId: ID!
    $n: Int!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(edge_id: $edgeId, n: $n) {
        id
        name
        display_name
        namespace
        data_source
        columns {
          id
          name
          display_name
          destinations
        }
        destinations
        all_destinations
        all_sources
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
    GetTablesAndEdgesEdgeLineage,
    GetTablesAndEdgesEdgeLineageVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
      edgeId: edge.id,
      n: value - 1,
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
      data-testid="edge-lineage"
    >
      <GraphComponent
        tables={tables}
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
