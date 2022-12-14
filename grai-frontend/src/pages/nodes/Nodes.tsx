import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import AppTopBar from "../../components/layout/AppTopBar"
import NodesTable from "../../components/nodes/NodesTable"
import NodesHeader from "../../components/nodes/NodesHeader"
import { GetNodes, GetNodesVariables } from "./__generated__/GetNodes"
import { useParams } from "react-router-dom"
import { Box } from "@mui/material"

const GET_NODES = gql`
  query GetNodes($workspaceId: ID!) {
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
  metadata: {
    node_type: string
  }
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

  if (error) return <p>Error : {error.message}</p>

  const nodes = data?.workspace?.nodes ?? []

  const handleRefresh = () => refetch()

  const tables = nodes.filter(node => node.metadata.node_type === "Table")

  const filteredNodes =
    (search
      ? tables.filter(node =>
          node.name.toLowerCase().includes(search.toLowerCase())
        )
      : tables) ?? []

  return (
    <>
      <AppTopBar />
      <NodesHeader
        search={search}
        onSearch={setSearch}
        onRefresh={handleRefresh}
      />
      <Box sx={{ px: 3 }}>
        <NodesTable nodes={filteredNodes} loading={loading} />
      </Box>
    </>
  )
}

export default Nodes
