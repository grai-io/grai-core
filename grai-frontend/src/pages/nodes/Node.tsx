import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import AppTopBar from "../../components/layout/AppTopBar"
import Loading from "../../components/layout/Loading"
import NotFound from "../NotFound"
import NodeHeader from "../../components/nodes/NodeHeader"
import NodeContent from "../../components/nodes/NodeContent"

const GET_NODE = gql`
  query GetNode($nodeId: ID!) {
    node(pk: $nodeId) {
      id
      namespace
      name
      displayName
      isActive
      dataSource
      sourceEdges {
        id
        isActive
        dataSource
        destination {
          id
          name
          displayName
          metadata
        }
        metadata
      }
      destinationEdges {
        id
        isActive
        dataSource
        source {
          id
          name
          displayName
          metadata
        }
        metadata
      }
      metadata
    }
  }
`

const Node: React.FC = () => {
  const params = useParams()

  const { loading, error, data } = useQuery(GET_NODE, {
    variables: {
      nodeId: params.nodeId,
    },
  })

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  const node = data.node

  if (!node) return <NotFound />

  return (
    <>
      <AppTopBar />
      <NodeHeader node={node} />
      <NodeContent node={node} />
    </>
  )
}

export default Node
