import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import React from "react"
import { nodesToTables } from "helpers/graph"
import theme from "theme"
import Loading from "components/layout/Loading"
import { Node as NodeType } from "helpers/graph"
import {
  GetNodesAndEdgesNodeLineage,
  GetNodesAndEdgesNodeLineageVariables,
} from "./__generated__/GetNodesAndEdgesNodeLineage"
import { useParams } from "react-router-dom"
import Graph from "components/graph/Graph"
import GraphError from "components/utils/GraphError"

const GET_NODES_AND_EDGES = gql`
  query GetNodesAndEdgesNodeLineage($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
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

interface Node extends NodeType {
  id: string
  display_name: string
}

type NodeLineageProps = {
  node: Node
}

const NodeLineage: React.FC<NodeLineageProps> = ({ node }) => {
  const { workspaceId } = useParams()
  const { loading, error, data } = useQuery<
    GetNodesAndEdgesNodeLineage,
    GetNodesAndEdgesNodeLineageVariables
  >(GET_NODES_AND_EDGES, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  if (!data?.workspace.nodes || !data.workspace.edges) return null

  const tables = nodesToTables(data.workspace.nodes, data.workspace.edges)

  const hiddenNodes = tables.filter(t => {
    if (t.id === node.id) return false

    return !(
      t.sourceTables.some(sourceTable => sourceTable.id === node.id) ||
      t.destinationTables.some(sourceTable => sourceTable.id === node.id)
    )
  })

  return (
    <Box
      sx={{
        height: "calc(100vh - 226px)",
        width: "100%",
        backgroundColor: theme.palette.grey[100],
        mt: 2,
      }}
    >
      <Graph
        tables={tables}
        nodes={data.workspace.nodes}
        edges={data.workspace.edges}
        initialHidden={hiddenNodes.map(n => n.id)}
      />
    </Box>
  )
}

export default NodeLineage
