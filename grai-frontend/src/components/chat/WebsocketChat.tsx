import React, { useEffect, useState } from "react"
import { useApolloClient } from "@apollo/client"
import { baseURL } from "client"
import useWebSocket from "react-use-websocket"
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
  const [savedLastMessage, setSavedLastMessage] = useState<number | null>(null)

  const { cache } = useApolloClient()

  const socketUrl = `${socketURL}/ws/chat/${workspace.id}/`

  const { sendJsonMessage, lastMessage } = useWebSocket(socketUrl)

  /* istanbul ignore next */
  const addMessage = (message: Message) =>
    cache.modify({
      id: cache.identify({
        id: chat.id,
        __typename: "Chat",
      }),
      fields: {
        messages: (existingMessages = { data: [] }) => ({
          data: existingMessages.data
            ? existingMessages.data.concat({
                id: self.crypto.randomUUID(),
                ...message,
                created_at: new Date().toISOString(),
                __typename: "Message",
              })
            : [],
        }),
      },
    })

  useEffect(() => {
    if (lastMessage !== null) {
      const message = lastMessage.timeStamp
      if (message != savedLastMessage) {
        addMessage({
          message: JSON.parse(lastMessage.data).message,
          role: "system",
        })
        setSavedLastMessage(message)
      }
    }
  }, [lastMessage, addMessage])

  const handleInput = (message: string) => {
    const msg = {
      type: "chat.message",
      message,
      chat_id: chat?.id,
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
