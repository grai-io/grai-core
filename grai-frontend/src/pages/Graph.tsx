import React from "react"
import { Alert, Box } from "@mui/material"
import GraphComponent, { Error } from "components/graph/Graph"
import { gql, useQuery } from "@apollo/client"
import theme from "theme"
import { useLocation, useParams } from "react-router-dom"
import { nodesToTables } from "helpers/graph"
import {
  GetNodesAndEdges,
  GetNodesAndEdgesVariables,
} from "./__generated__/GetNodesAndEdges"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"

export const GET_NODES_AND_EDGES = gql`
  query GetNodesAndEdges($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      nodes {
        id
        namespace
        name
        display_name
        data_source
        metadata
      }
      edges {
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

const Graph: React.FC = () => {
  const { workspaceId } = useParams()
  const searchParams = new URLSearchParams(useLocation().search)

  const { loading, error, data } = useQuery<
    GetNodesAndEdges,
    GetNodesAndEdgesVariables
  >(GET_NODES_AND_EDGES, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const errorsQS = searchParams.get("errors")
  const errors: Error[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  if (!data?.workspace.nodes) return <Alert>No nodes found</Alert>

  const tables = nodesToTables(data.workspace.nodes, data.workspace.edges)

  return (
    <PageLayout>
      <Box
        sx={{
          height: "calc(100vh - 70px)",
          width: "100%",
          backgroundColor: theme.palette.grey[100],
        }}
      >
        <GraphComponent
          tables={tables}
          nodes={data.workspace.nodes}
          edges={data.workspace.edges}
          errors={errors}
          limitGraph={limitGraph}
        />
      </Box>
    </PageLayout>
  )
}

export default Graph
