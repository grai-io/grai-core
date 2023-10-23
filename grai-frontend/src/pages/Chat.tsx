import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box, Grid, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import WebsocketChat from "components/chat/WebsocketChat"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceChat,
  GetWorkspaceChatVariables,
  GetWorkspaceChat_workspace_chats_data_messages_data,
} from "./__generated__/GetWorkspaceChat"
import NotFound from "./NotFound"
import { Chat as ChatType } from "components/chat/ChatWindow"

export const GET_WORKSPACE = gql`
  query GetWorkspaceChat($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      chats {
        data {
          id
          messages {
            data {
              id
              message
              role
              created_at
            }
          }
        }
      }
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

  const chats: ChatType[] = workspace.chats.data
    .reduce<GetWorkspaceChat_workspace_chats_data_messages_data[]>(
      (acc, chat) => {
        return acc.concat(chat.messages.data)
      },
      [],
    )
    .map(message => ({
      message: message.message,
      sender: message.role === "USER",
    }))
  const chatId = workspace.chats.data.at(-1)?.id

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h6">GrAI Workspace Chat</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <WebsocketChat
            workspace={workspace}
            initialChats={chats}
            initialChatId={chatId}
          />
        </Grid>
      </Grid>
    </Box>
  )
}

export default Chat
