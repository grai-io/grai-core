import React from "react"
import { Box } from "@mui/material"
import Graph from "../components/home/Graph"
import AppTopBar from "../components/layout/AppTopBar"
import { gql, useQuery } from "@apollo/client"
import Loading from "../components/layout/Loading"

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

const Home: React.FC = () => {
  const { loading, error, data } = useQuery(GET_NODES_AND_EDGES)

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  return (
    <>
      <AppTopBar />
      {data.nodes && data.edges && (
        <Box sx={{ height: "calc(100vh - 68px)", width: "100%" }}>
          <Graph nodes={data.nodes} edges={data.edges} />
        </Box>
      )}
    </>
  )
}

export default Home
