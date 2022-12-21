import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import AppTopBar from "components/layout/AppTopBar"
import Loading from "components/layout/Loading"
import NotFound from "pages/NotFound"
import NodeHeader from "components/nodes/NodeHeader"
import NodeContent from "components/nodes/NodeContent"
import { GetNode, GetNodeVariables } from "./__generated__/GetNode"
import GraphError from "components/utils/GraphError"

const GET_NODE = gql`
  query GetNode($workspaceId: ID!, $nodeId: ID!) {
    workspace(pk: $workspaceId) {
      id
      node(pk: $nodeId) {
        id
        namespace
        name
        display_name
        is_active
        data_source
        metadata
      }
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

  if (error) return <GraphError error={error} />
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
