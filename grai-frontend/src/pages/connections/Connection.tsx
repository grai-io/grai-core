import { gql, useQuery } from "@apollo/client"
import { MoreHoriz } from "@mui/icons-material"
import { Box, Button, Grid, Stack, Typography } from "@mui/material"
import React from "react"
import { useParams } from "react-router-dom"
import ConnectionRefresh from "components/connections/ConnectionRefresh"
import UpdateConnectionForm from "components/connections/UpdateConnectionForm"
import AppTopBar from "components/layout/AppTopBar"
import Loading from "components/layout/Loading"
import NotFound from "pages/NotFound"
import {
  GetConnection,
  GetConnectionVariables,
} from "./__generated__/GetConnection"
import GraphError from "components/utils/GraphError"

const GET_CONNECTION = gql`
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
  if (loading)
    return (
      <>
        <AppTopBar />
        <Loading />
      </>
    )

  const connection = data?.workspace?.connection

  if (!connection) return <NotFound />

  return (
    <>
      <AppTopBar />
      <Box sx={{ display: "flex", p: 3 }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          {connection.name}
        </Typography>
        <Stack direction="row" spacing={1}>
          <ConnectionRefresh connection={connection} />
          <Button variant="outlined" sx={{ minWidth: 0 }}>
            <MoreHoriz />
          </Button>
        </Stack>
      </Box>
      <Grid container sx={{ px: 3 }}>
        <Grid item md={4}>
          <UpdateConnectionForm connection={connection} />
        </Grid>
      </Grid>
    </>
  )
}

export default Connection
