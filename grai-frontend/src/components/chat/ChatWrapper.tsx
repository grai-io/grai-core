import React from "react"
import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import WebsocketChat from "./WebsocketChat"
import { LastChat, LastChatVariables } from "./__generated__/LastChat"

export const FETCH_CHAT = gql`
  query LastChat($workspaceId: ID!) {
    workspace(id: $workspaceId) {
      id
      last_chat {
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
  const { data, loading, error } = useQuery<LastChat, LastChatVariables>(
    FETCH_CHAT,
    {
      variables: {
        workspaceId: workspace.id,
      },
    },
  )

  if (error) return <GraphError error={error} />
  if (loading || !data) return <Loading />

  return <WebsocketChat workspace={workspace} chat={data.workspace.last_chat} />
}

export default ChatWrapper
