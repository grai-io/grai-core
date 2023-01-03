import React from "react"
import { Box } from "@mui/material"
import GraphComponent, { Error } from "components/graph/Graph"
import AppTopBar from "components/layout/AppTopBar"
import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import theme from "theme"
import { useLocation, useParams } from "react-router-dom"
import { nodesToTables } from "helpers/graph"
import {
  GetNodesAndEdges,
  GetNodesAndEdgesVariables,
} from "./__generated__/GetNodesAndEdges"
import GraphError from "components/utils/GraphError"

export const GET_NODES_AND_EDGES = gql`
  query GetNodesAndEdges($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      nodes {
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
  if (loading)
    return (
      <>
        <AppTopBar />
        <Loading />
      </>
    )

  const errorsQS = searchParams.get("errors")
  const errors: Error[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  if (!data?.workspace.nodes) return null

  const tables = nodesToTables(data.workspace.nodes, data.workspace.edges)

  return (
    <>
      <AppTopBar />

      <Box
        sx={{
          height: "calc(100vh - 70px)",
          width: "100%",
          backgroundColor: theme.palette.grey[100],
        }}
      >
        <GraphComponent
          tables={tables}
          edges={data.workspace.edges}
          errors={errors}
          limitGraph={limitGraph}
        />
      </Box>
    </>
  )
}

export default Graph
