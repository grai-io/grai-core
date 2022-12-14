import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import AppTopBar from "../../components/layout/AppTopBar"
import Loading from "../../components/layout/Loading"
import NotFound from "../NotFound"
import NodeHeader from "../../components/nodes/NodeHeader"
import NodeContent from "../../components/nodes/NodeContent"
import { GetNode, GetNodeVariables } from "./__generated__/GetNode"

const GET_NODE = gql`
  query GetNode($workspaceId: ID!, $nodeId: ID!) {
    workspace(pk: $workspaceId) {
      id
      node(pk: $nodeId) {
        id
        namespace
        name
        displayName
        isActive
        dataSource
        metadata
      }
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

const Node: React.FC = () => {
  const { workspaceId, nodeId } = useParams()

  const { loading, error, data } = useQuery<GetNode, GetNodeVariables>(
    GET_NODE,
    {
      variables: {
        workspaceId: workspaceId ?? "",
        nodeId: nodeId ?? "",
      },
    }
  )

  if (error) return <p>Error : {error.message}</p>
  if (loading)
    return (
      <>
        <AppTopBar />
        <Loading />
      </>
    )

  const node = data?.workspace?.node

  if (!node) return <NotFound />

  return (
    <>
      <AppTopBar />
      <NodeHeader node={node} />
      <NodeContent
        node={node}
        nodes={data?.workspace?.nodes}
        edges={data?.workspace?.edges}
      />
    </>
  )
}

export default Node
