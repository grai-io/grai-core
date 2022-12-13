import React from "react"
import { Box } from "@mui/material"
import GraphComponent, { Error } from "../components/graph/Graph"
import AppTopBar from "../components/layout/AppTopBar"
import { gql, useQuery } from "@apollo/client"
import Loading from "../components/layout/Loading"
import theme from "../theme"
import { useLocation } from "react-router-dom"
import { nodesToTables } from "../helpers/graph"

const GET_NODES_AND_EDGES = gql`
  query GetNodesAndEdges {
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
        name
        displayName
      }
      destination {
        id
        name
        displayName
      }
      metadata
    }
  }
`

const Graph: React.FC = () => {
  const searchParams = new URLSearchParams(useLocation().search)

  const { loading, error, data } = useQuery(GET_NODES_AND_EDGES)

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

  const tables = nodesToTables(data.nodes, data.edges)

  return (
    <>
      <AppTopBar />
      {data.nodes && data.edges && (
        <Box
          sx={{
            height: "calc(100vh - 70px)",
            width: "100%",
            backgroundColor: theme.palette.grey[100],
          }}
        >
          <GraphComponent
            tables={tables}
            edges={data.edges}
            errors={errors}
            limitGraph={limitGraph}
          />
        </Box>
      )}
    </>
  )
}

export default Graph
