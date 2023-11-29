import React, { createContext, useCallback, useState } from "react"
import { gql, useApolloClient } from "@apollo/client"
import { baseURL } from "client"
import useWebSocket from "react-use-websocket"
import { NewMessage } from "./__generated__/NewMessage"

const socketURL =
  window._env_?.REACT_APP_SERVER_WS_URL ??
  process.env.REACT_APP_SERVER_WS_URL ??
  baseURL.replace("http", "ws")

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

interface RoleMessage {
  message: string
  role: string
}

export type Message = {
  message: string
  sender: boolean
}

type ChatContextType = {
  unread: boolean
  messages: Message[]
  sendMessage: (message: string) => void
  clearUnread: () => void
  workspace: Workspace
}

/* istanbul ignore next */
export const ChatContext = createContext<ChatContextType>({
  unread: false,
  messages: [],
  sendMessage: () => {},
  clearUnread: () => {},
  workspace: { id: "" },
})

type ChatProviderProps = {
  workspace: Workspace
  chat: Chat
  children?: React.ReactNode
}

const ChatProvider: React.FC<ChatProviderProps> = ({
  workspace,
  chat,
  children,
}) => {
  const [unread, setUnread] = useState(false)

  const { cache } = useApolloClient()

  const socketUrl = `${socketURL}/ws/chat/${workspace.id}/`

  const { sendJsonMessage } = useWebSocket(socketUrl, {
    onMessage: event => {
      const data = JSON.parse(event.data)

      addMessage({
        message: data.message,
        role: data.role,
      })
      setUnread(true)
    },
  })

  const addMessage = useCallback(
    (message: RoleMessage) =>
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

  const sendMessage = (message: string) => {
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

  const clearUnread = () => setUnread(false)

  const value = {
    unread,
    messages,
    sendMessage,
    clearUnread,
    workspace,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}

export default ChatProvider
