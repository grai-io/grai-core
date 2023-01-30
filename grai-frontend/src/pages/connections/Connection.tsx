import { gql, useQuery } from "@apollo/client"
import React from "react"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import {
  GetConnection,
  GetConnectionVariables,
} from "./__generated__/GetConnection"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import ConnectionHeader from "components/connections/ConnectionHeader"
import ConnectionContent from "components/connections/ConnectionContent"
import ConnectionTabs from "components/connections/ConnectionTabs"
import useWorkspace from "helpers/useWorkspace"
import useRunPolling from "helpers/runPolling"

export const GET_CONNECTION = gql`
  query GetConnection(
    $organisationName: String!
    $workspaceName: String!
    $connectionId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      connection(id: $connectionId) {
        id
        namespace
        name
        connector {
          id
          name
          metadata
        }
        metadata
        schedules
        is_active
        created_at
        updated_at
        last_run {
          id
          status
          created_at
          started_at
          finished_at
          metadata
          user {
            id
            first_name
            last_name
          }
        }
        last_successful_run {
          id
          status
          created_at
          started_at
          finished_at
          metadata
          user {
            id
            first_name
            last_name
          }
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
      }
    }
  }
`

const Connection: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { connectionId } = useParams()

  const { loading, error, data, startPolling, stopPolling } = useQuery<
    GetConnection,
    GetConnectionVariables
  >(GET_CONNECTION, {
    variables: {
      organisationName,
      workspaceName,
      connectionId: connectionId ?? "",
    },
  })

  const status = data?.workspace.connection?.last_run?.status

  useRunPolling(status, startPolling, stopPolling)

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const connection = data?.workspace?.connection

  if (!connection) return <NotFound />

  const handleRefresh = () => startPolling(1000)

  return (
    <PageLayout>
      <ConnectionHeader
        connection={connection}
        workspaceId={data.workspace.id}
        onRefresh={handleRefresh}
      />
      <ConnectionContent connection={connection} />
      <ConnectionTabs connection={connection} />
    </PageLayout>
  )
}

export default Connection
