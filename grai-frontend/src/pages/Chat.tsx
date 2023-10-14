import { gql, useQuery } from "@apollo/client"
import { Box, Grid, Typography } from "@mui/material"
import WebsocketChat from "components/chat/WebsocketChat"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import React from "react"
import NotFound from "./NotFound"
import {
  GetWorkspaceChat,
  GetWorkspaceChatVariables,
} from "./__generated__/GetWorkspaceChat"

export const GET_WORKSPACE = gql`
  query GetWorkspaceChat($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
    }
  }
`

const Chat: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceChat,
    GetWorkspaceChatVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h6">GrAI Workspace Chat</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <WebsocketChat workspace={workspace} />
        </Grid>
      </Grid>
    </Box>
  )
}

export default Chat
