import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetConnectionCreate,
  GetConnectionCreateVariables,
} from "./__generated__/GetConnectionCreate"
import SetupConnection from "./SetupConnection"

export const GET_CONNECTION = gql`
  query GetConnectionCreate($workspaceId: ID!, $connectionId: ID!) {
    workspace(id: $workspaceId) {
      id
      connection(id: $connectionId) {
        id
        connector {
          id
          name
          icon
          metadata
        }
        source {
          id
          name
        }
        last_run {
          id
          status
        }
        namespace
        name
        metadata
        is_active
        created_at
        updated_at
      }
    }
  }
`

type UpdateConnectionTabProps = {
  workspaceId: string
  connectionId: string
}

const UpdateConnectionTab: React.FC<UpdateConnectionTabProps> = ({
  workspaceId,
  connectionId,
}) => {
  const { loading, error, data } = useQuery<
    GetConnectionCreate,
    GetConnectionCreateVariables
  >(GET_CONNECTION, {
    variables: {
      workspaceId,
      connectionId,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const connection = data?.workspace?.connection

  if (!connection) return <NotFound />

  return (
    <SetupConnection
      workspaceId={workspaceId}
      connector={connection.connector}
      connection={{
        ...connection,
        sourceName: connection.source.name,
        secrets: null,
      }}
    />
  )
}

export default UpdateConnectionTab
