import React from "react"
import { gql, useQuery } from "@apollo/client"
import ConnectionsTable from "components/connections/ConnectionsTable"
import ConnectionsHeader from "components/connections/ConnectionsHeader"
import {
  GetConnections,
  GetConnectionsVariables,
} from "./__generated__/GetConnections"
import { Box } from "@mui/material"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import useWorkspace from "helpers/useWorkspace"

export const GET_CONNECTIONS = gql`
  query GetConnections($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
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
        runs(order: { created_at: DESC }) {
          id
          status
          created_at
          started_at
          finished_at
          user {
            id
            first_name
            last_name
          }
          metadata
        }
        last_run {
          id
          status
          created_at
          started_at
          finished_at
          user {
            id
            first_name
            last_name
          }
          metadata
        }
        last_successful_run {
          id
          status
          created_at
          started_at
          finished_at
          user {
            id
            first_name
            last_name
          }
          metadata
        }
      }
    }
  }
`

const Connections: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data, refetch } = useQuery<
    GetConnections,
    GetConnectionsVariables
  >(GET_CONNECTIONS, {
    variables: {
      organisationName,
      workspaceName,
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
          workspaceId={data?.workspace.id}
          loading={loading}
        />
      </Box>
    </PageLayout>
  )
}

export default Connections
