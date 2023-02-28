import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import ConnectionsHeader from "components/connections/ConnectionsHeader"
import ConnectionsTable from "components/connections/ConnectionsTable"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetConnections,
  GetConnectionsVariables,
} from "./__generated__/GetConnections"

//Extra parameters required to make cache update work on connection run
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
