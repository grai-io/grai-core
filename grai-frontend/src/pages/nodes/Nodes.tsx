import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import AppTopBar from "../../components/layout/AppTopBar"
import NodesTable from "../../components/nodes/NodesTable"
import NodesHeader from "../../components/nodes/NodesHeader"
import { GetNodes } from "./__generated__/GetNodes"

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
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<GetNodes>(GET_NODES)

  if (error) return <p>Error : {error.message}</p>

  const handleRefresh = () => refetch()

  const filteredNodes =
    (search
      ? data?.nodes.filter((node: any) =>
          node.name.toLowerCase().includes(search.toLowerCase())
        )
      : data?.nodes) ?? []

  return (
    <>
      <AppTopBar />
      <NodesHeader
        search={search}
        onSearch={setSearch}
        onRefresh={handleRefresh}
      />
      <NodesTable nodes={filteredNodes} loading={loading} />
    </>
  )
}

export default Nodes
