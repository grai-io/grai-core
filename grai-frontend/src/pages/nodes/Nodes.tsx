import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import AppTopBar from "../../components/layout/AppTopBar"
import NodesTable from "../../components/nodes/NodesTable"
import Loading from "../../components/layout/Loading"

const GET_NODES = gql`
  query GetNodes {
    nodes {
      id
      namespace
      name
      displayName
      isActive
      dataSource
      metadata
    }
  }
`

export interface Node {
  id: string
  namespace: string
  name: string
  displayName: string
  dataSource: string
  isActive: boolean
  metadata: any
}

const Nodes: React.FC = () => {
  const { loading, error, data } = useQuery(GET_NODES)

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  return (
    <>
      <AppTopBar />
      <Typography variant="h4" sx={{ textAlign: "center", m: 3 }}>
        Nodes
      </Typography>
      <NodesTable nodes={data.nodes ?? null} />
    </>
  )
}

export default Nodes
