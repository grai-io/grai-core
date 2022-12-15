import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import EdgesTable from "components/edges/EdgesTable"
import AppTopBar from "components/layout/AppTopBar"
import { Node } from "pages/nodes/Nodes"
import Loading from "components/layout/Loading"
import { GetEdges, GetEdgesVariables } from "./__generated__/GetEdges"
import { useParams } from "react-router-dom"
import GraphError from "components/utils/GraphError"

const GET_EDGES = gql`
  query GetEdges($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
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

export interface Edge {
  id: string
  dataSource: string
  isActive: boolean
  source: Node
  destination: Node
  metadata: any
}

const Edges: React.FC = () => {
  const { workspaceId } = useParams()
  const { loading, error, data } = useQuery<GetEdges, GetEdgesVariables>(
    GET_EDGES,
    {
      variables: {
        workspaceId: workspaceId ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const edges = data?.workspace?.edges ?? []

  return (
    <>
      <AppTopBar />
      <Typography variant="h4" sx={{ textAlign: "center", m: 3 }}>
        Edges
      </Typography>
      <EdgesTable edges={edges} />
      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Edges
