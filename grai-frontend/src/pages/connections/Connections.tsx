import React from "react"
import { gql, useQuery } from "@apollo/client"
import ConnectionsTable from "components/connections/ConnectionsTable"
import ConnectionsHeader from "components/connections/ConnectionsHeader"
import {
  GetConnections,
  GetConnectionsVariables,
} from "./__generated__/GetConnections"
import { useParams } from "react-router-dom"
import { Box } from "@mui/material"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"

export const GET_CONNECTIONS = gql`
  query GetConnections($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      connections {
        id
        namespace
        name
        is_active
        connector {
          id
          name
        }
        last_run {
          id
          status
          started_at
          finished_at
          metadata
        }
        last_successful_run {
          id
          status
          started_at
          finished_at
          metadata
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

  if (error) return <GraphError error={error} />

  return (
    <PageLayout>
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
    </PageLayout>
  )
}

export default Connections
