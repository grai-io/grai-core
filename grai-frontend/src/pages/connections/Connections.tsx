import React from "react"
import { gql, useQuery } from "@apollo/client"
import AppTopBar from "../../components/layout/AppTopBar"
import ConnectionsTable from "../../components/connections/ConnectionsTable"
import ConnectionsHeader from "../../components/connections/ConnectionsHeader"
import { GetConnections } from "./__generated__/GetConnections"

const GET_CONNECTIONS = gql`
  query GetConnections {
    connections {
      id
      namespace
      name
      connector {
        id
        name
      }
    }
  }
`

const Connections: React.FC = () => {
  const { loading, error, data, refetch } =
    useQuery<GetConnections>(GET_CONNECTIONS)

  const handleRefresh = () => refetch()

  if (error) return <p>Error : {error.message}</p>

  return (
    <>
      <AppTopBar />
      <ConnectionsHeader onRefresh={handleRefresh} />
      <ConnectionsTable
        connections={data?.connections ?? []}
        loading={loading}
      />
    </>
  )
}

export default Connections
