import React, { useEffect, useState } from "react"
import { baseURL } from "client"
import useWebSocket from "react-use-websocket"
import ChatWindow from "./ChatWindow"

const socketURL =
  window._env_?.REACT_APP_SERVER_WS_URL ??
  process.env.REACT_APP_SERVER_WS_URL ??
  baseURL.replace("http", "ws")

interface Message {
  message: string
  sender: boolean
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
  chat?: Chat
}

const WebsocketChat: React.FC<WebsocketChatProps> = ({ workspace, chat }) => {
  const [messages, setMessages] = useState<Message[]>([])

  const socketUrl = `${socketURL}/ws/chat/${workspace.id}/`

  const { sendJsonMessage, lastMessage } = useWebSocket(socketUrl)

  useEffect(() => {
    if (lastMessage !== null)
      setMessages(prev =>
        prev.concat({
          message: JSON.parse(lastMessage.data).message,
          sender: false,
        }),
      )
  }, [lastMessage, setMessages])

  useEffect(() => {
    if (!chat) return

    const initialMessages: Message[] =
      chat.messages.data.map(m => ({
        message: m.message,
        sender: m.role === "user",
      })) ?? []

    setMessages(initialMessages)
  }, [chat, setMessages])

  const handleInput = (message: string) => {
    const msg = {
      type: "chat.message",
      message,
      chat_id: chat?.id,
    }
    sendJsonMessage(msg)
    setMessages(prev => [...prev, { message, sender: true }])
  }

  return (
    <ChatWindow
      messages={messages}
      onInput={handleInput}
      workspaceId={workspace.id}
    />
  )
}

export default WebsocketChat
