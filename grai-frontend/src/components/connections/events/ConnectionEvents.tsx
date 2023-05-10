import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import PageContent from "components/layout/PageContent"
import GraphError from "components/utils/GraphError"
import {
  GetConnectionEvents,
  GetConnectionEventsVariables,
} from "./__generated__/GetConnectionEvents"
import ConnectionEventsTable from "./ConnectionEventsTable"

export const GET_CONNECTION_EVENTS = gql`
  query GetConnectionEvents(
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
          icon
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
        events {
          data {
            id
            status
            created_at
            metadata
          }
          meta {
            total
          }
        }
      }
    }
  }
`

interface Connection {
  id: string
}

type ConnectionEventsProps = {
  connection: Connection
}

const ConnectionEvents: React.FC<ConnectionEventsProps> = ({ connection }) => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetConnectionEvents,
    GetConnectionEventsVariables
  >(GET_CONNECTION_EVENTS, {
    variables: {
      organisationName,
      workspaceName,
      connectionId: connection.id,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const connectionData = data?.workspace?.connection

  if (!connectionData) return <NotFound />

  const events = connectionData.events.data

  return (
    <>
      <PageContent>
        <h1>Connection Graph</h1>
      </PageContent>
      <PageContent>
        <ConnectionEventsTable
          events={events}
          total={connectionData.events.meta.total}
        />
      </PageContent>
    </>
  )
}

export default ConnectionEvents
