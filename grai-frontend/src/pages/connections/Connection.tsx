import { gql, useQuery } from "@apollo/client"
import { Grid } from "@mui/material"
import React from "react"
import { useParams } from "react-router-dom"
import UpdateConnectionForm from "components/connections/UpdateConnectionForm"
import NotFound from "pages/NotFound"
import {
  GetConnection,
  GetConnectionVariables,
} from "./__generated__/GetConnection"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import ConnectionHeader from "components/connections/ConnectionHeader"

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
      <Grid container sx={{ px: 3 }}>
        <Grid item md={4}>
          <UpdateConnectionForm connection={connection} />
        </Grid>
      </Grid>
    </PageLayout>
  )
}

export default Connection
