import React, { useEffect } from "react"
import { gql, useMutation } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  FetchChats,
  FetchChatsVariables,
  FetchChats_fetchOrCreateChats_data_messages_data,
} from "./__generated__/FetchChats"
import { Chat } from "./ChatWindow"
import WebsocketChat from "./WebsocketChat"

export const FETCH_CHATS = gql`
  mutation FetchChats($workspaceId: ID!) {
    fetchOrCreateChats(workspaceId: $workspaceId) {
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
`

interface Workspace {
  id: string
}

type ChatWrapperProps = {
  workspace: Workspace
}

const ChatWrapper: React.FC<ChatWrapperProps> = ({ workspace }) => {
  const [fetchChats, { data, loading, error }] = useMutation<
    FetchChats,
    FetchChatsVariables
  >(FETCH_CHATS, {
    variables: {
      workspaceId: workspace.id,
    },
  })

  useEffect(() => {
    fetchChats().catch(() => {})
  }, [fetchChats])

  if (error) return <GraphError error={error} />
  if (loading || !data) return <Loading />

  const chats: Chat[] = data.fetchOrCreateChats.data
    .reduce<FetchChats_fetchOrCreateChats_data_messages_data[]>((acc, chat) => {
      return acc.concat(chat.messages.data)
    }, [])
    .map(message => ({
      message: message.message,
      sender: message.role === "USER",
    }))
  const chatId = data.fetchOrCreateChats.data.at(-1)?.id

  return (
    <WebsocketChat
      workspace={workspace}
      initialChats={chats}
      initialChatId={chatId}
    />
  )
}

export default ChatWrapper
