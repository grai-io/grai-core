import React, { useCallback } from "react"
import { gql, useApolloClient } from "@apollo/client"
import { baseURL } from "client"
import useWebSocket from "react-use-websocket"
import { NewMessage } from "./__generated__/NewMessage"
import ChatWindow from "./ChatWindow"

const socketURL =
  window._env_?.REACT_APP_SERVER_WS_URL ??
  process.env.REACT_APP_SERVER_WS_URL ??
  baseURL.replace("http", "ws")

interface Message {
  message: string
  role: string
}

interface Workspace {
  id: string
}

interface Chat {
  id: string
  messages: {
    data: {
      id: string
      message: string
      role: string
      created_at: string
    }[]
  }
}

type WebsocketChatProps = {
  workspace: Workspace
  chat: Chat
}

const WebsocketChat: React.FC<WebsocketChatProps> = ({ workspace, chat }) => {
  const { cache } = useApolloClient()

  const socketUrl = `${socketURL}/ws/chat/${workspace.id}/`

  const { sendJsonMessage } = useWebSocket(socketUrl, {
    onMessage: event => {
      addMessage({
        message: JSON.parse(event.data).message,
        role: "system",
      })
    },
  })

  const addMessage = useCallback(
    (message: Message) =>
      cache.modify({
        id: cache.identify({
          id: chat.id,
          __typename: "Chat",
        }),
        fields: {
          /* istanbul ignore next */
          messages(existingMessages = { data: [] }) {
            const newMessage = cache.writeFragment<NewMessage>({
              data: {
                id: crypto.randomUUID(),
                ...message,
                created_at: new Date().toISOString(),
                __typename: "Message",
              },
              fragment: gql`
                fragment NewMessage on Message {
                  id
                  message
                  role
                  created_at
                }
              `,
            })
            return { data: [...existingMessages.data, newMessage] }
          },
        },
      }),
    [cache, chat.id],
  )

  const handleInput = (message: string) => {
    const msg = {
      type: "chat.message",
      message,
      chat_id: chat.id,
    }
    sendJsonMessage(msg)
    addMessage({ message, role: "user" })
  }

  const messages = chat.messages.data.map(message => ({
    message: message.message,
    sender: message.role === "user",
  }))

  return (
    <ChatWindow
      messages={messages}
      onInput={handleInput}
      workspaceId={workspace.id}
    />
  )
}

export default WebsocketChat
