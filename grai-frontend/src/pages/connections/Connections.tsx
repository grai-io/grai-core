import React from "react"
import { gql, useQuery } from "@apollo/client"
import AppTopBar from "components/layout/AppTopBar"
import ConnectionsTable from "components/connections/ConnectionsTable"
import ConnectionsHeader from "components/connections/ConnectionsHeader"
import {
  GetConnections,
  GetConnectionsVariables,
} from "./__generated__/GetConnections"
import { useParams } from "react-router-dom"
import { Box } from "@mui/material"

const GET_CONNECTIONS = gql`
  query GetConnections($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
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
  }
`

const Connections: React.FC = () => {
  const { workspaceId } = useParams()

  const { loading, error, data, refetch } = useQuery<
    GetConnections,
    GetConnectionsVariables
  >(GET_CONNECTIONS, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  const handleRefresh = () => refetch()

  if (error) return <p>Error : {error.message}</p>

  return (
    <>
      <AppTopBar />
      <ConnectionsHeader onRefresh={handleRefresh} />
      <Box
        sx={{
          px: 3,
        }}
      >
        <ConnectionsTable
          connections={data?.workspace.connections ?? []}
          loading={loading}
        />
      </Box>
    </>
  )
}

export default Connections
