import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import React from "react"
import { nodesToTables } from "../../helpers/graph"
import theme from "../../theme"
import Graph from "../graph/Graph"
import Loading from "../layout/Loading"
import { Node as NodeType } from "../../helpers/graph"
import {
  GetNodesAndEdgesNodeLineage,
  GetNodesAndEdgesNodeLineageVariables,
} from "./__generated__/GetNodesAndEdgesNodeLineage"
import { useParams } from "react-router-dom"

const GET_NODES_AND_EDGES = gql`
  query GetNodesAndEdgesNodeLineage($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
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

interface Node extends NodeType {
  id: string
  displayName: string
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

  if (error) return <p>Error : {error.message}</p>
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
        edges={data.workspace.edges}
        initialHidden={hiddenNodes.map(n => n.id)}
      />
    </Box>
  )
}

export default NodeLineage
