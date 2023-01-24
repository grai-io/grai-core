import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import NodeHeader from "components/nodes/NodeHeader"
import NodeContent from "components/nodes/NodeContent"
import { GetNode, GetNodeVariables } from "./__generated__/GetNode"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import useWorkspace from "helpers/useWorkspace"

export const GET_NODE = gql`
  query GetNode(
    $organisationName: String!
    $workspaceName: String!
    $nodeId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      node(id: $nodeId) {
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
  const { organisationName, workspaceName } = useWorkspace()
  const { nodeId } = useParams()

  const { loading, error, data } = useQuery<GetNode, GetNodeVariables>(
    GET_NODE,
    {
      variables: {
        organisationName,
        workspaceName,
        nodeId: nodeId ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const node = data?.workspace?.node

  if (!node) return <NotFound />

  return (
    <PageLayout>
      <NodeHeader node={node} />
      <NodeContent
        node={node}
        nodes={data?.workspace?.nodes}
        edges={data?.workspace?.edges}
      />
    </PageLayout>
  )
}

export default Node
