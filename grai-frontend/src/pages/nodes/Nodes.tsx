import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import NodesTable from "components/nodes/NodesTable"
import NodesHeader from "components/nodes/NodesHeader"
import { GetNodes, GetNodesVariables } from "./__generated__/GetNodes"
import { useParams } from "react-router-dom"
import { Box } from "@mui/material"
import GraphError from "components/utils/GraphError"
import { nodeIsTable } from "helpers/graph"
import PageLayout from "components/layout/PageLayout"

export const GET_NODES = gql`
  query GetNodes($workspaceId: ID!) {
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
    }
  }
`

export interface Node {
  id: string
  namespace: string
  name: string
  display_name: string
  data_source: string
  is_active: boolean
}

const Nodes: React.FC = () => {
  const { workspaceId } = useParams()
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<
    GetNodes,
    GetNodesVariables
  >(GET_NODES, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />

  const nodes = data?.workspace?.nodes ?? []

  const handleRefresh = () => refetch()

  const tables = nodes.filter(nodeIsTable)

  const filteredNodes = search
    ? tables.filter(node =>
        node.name.toLowerCase().includes(search.toLowerCase())
      )
    : tables

  return (
    <PageLayout>
      <NodesHeader
        search={search}
        onSearch={setSearch}
        onRefresh={handleRefresh}
      />
      <Box sx={{ px: 3 }}>
        <NodesTable nodes={filteredNodes} loading={loading} />
      </Box>
    </PageLayout>
  )
}

export default Nodes
