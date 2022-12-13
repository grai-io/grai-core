import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import EdgesTable from "../../components/edges/EdgesTable"
import AppTopBar from "../../components/layout/AppTopBar"
import { Node } from "../../pages/nodes/Nodes"
import Loading from "../../components/layout/Loading"
import { GetEdges } from "./__generated__/GetEdges"

const GET_EDGES = gql`
  query GetEdges {
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
  const { loading, error, data } = useQuery<GetEdges>(GET_EDGES)

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  return (
    <>
      <AppTopBar />
      <Typography variant="h4" sx={{ textAlign: "center", m: 3 }}>
        Edges
      </Typography>
      <EdgesTable edges={data?.edges ?? null} />
      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Edges
