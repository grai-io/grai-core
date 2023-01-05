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

export const GET_CONNECTION = gql`
  query GetConnection($workspaceId: ID!, $connectionId: ID!) {
    workspace(pk: $workspaceId) {
      id
      connection(pk: $connectionId) {
        id
        namespace
        name
        connector {
          id
          name
          metadata
        }
        metadata
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
  const { workspaceId, connectionId } = useParams()

  const { loading, error, data } = useQuery<
    GetConnection,
    GetConnectionVariables
  >(GET_CONNECTION, {
    variables: {
      workspaceId: workspaceId ?? "",
      connectionId: connectionId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const connection = data?.workspace?.connection

  if (!connection) return <NotFound />

  return (
    <PageLayout>
      <ConnectionHeader connection={connection} />
      <ConnectionContent connection={connection} />
    </PageLayout>
  )
}

export default Connection
