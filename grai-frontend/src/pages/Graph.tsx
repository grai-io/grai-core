import React from "react"
import { Box } from "@mui/material"
import GraphComponent, { Error } from "../components/graph/Graph"
import AppTopBar from "../components/layout/AppTopBar"
import { gql, useQuery } from "@apollo/client"
import Loading from "../components/layout/Loading"
import theme from "../theme"
import { useLocation, useParams } from "react-router-dom"
import { nodesToTables } from "../helpers/graph"
import {
  GetNodesAndEdges,
  GetNodesAndEdgesVariables,
} from "./__generated__/GetNodesAndEdges"

const GET_NODES_AND_EDGES = gql`
  query GetNodesAndEdges($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      nodes {
        id
        namespace
        name
        displayName
        isActive
        dataSource
        metadata
      }
      edges {
        id
        isActive
        dataSource
        source {
          id
          namespace
          name
          displayName
          dataSource
          isActive
          metadata
        }
        destination {
          id
          namespace
          name
          displayName
          dataSource
          isActive
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

  if (error) return <p>Error : {error.message}</p>
  if (loading)
    return (
      <>
        <AppTopBar />
        <Loading />
      </>
    )

  const errors: Error[] | null = searchParams.has("errors")
    ? JSON.parse(searchParams.get("errors") ?? "")
    : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  if (!data?.workspace?.nodes) return null

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
