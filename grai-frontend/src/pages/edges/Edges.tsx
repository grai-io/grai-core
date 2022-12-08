import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import EdgesTable from "../../components/edges/EdgesTable"
import AppTopBar from "../../components/layout/AppTopBar"
import { Node } from "../../pages/nodes/Nodes"

const GET_EDGES = gql`
  query GetEdges {
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

export interface Edge {
  id: string
  dataSource: string
  isActive: boolean
  source: Node
  destination: Node
  metadata: any
}

const Edges: React.FC = () => {
  const { loading, error, data } = useQuery(GET_EDGES)

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <p>Loading...</p>

  return (
    <>
      <AppTopBar />
      <Typography variant="h4" sx={{ textAlign: "center", m: 3 }}>
        Edges
      </Typography>
      <EdgesTable edges={data.edges ?? null} />
      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Edges
