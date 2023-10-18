import React, { useEffect, useState } from "react"
import { baseURL } from "client"
import useWebSocket from "react-use-websocket"
import ChatWindow, { Chat } from "./ChatWindow"

const socketURL =
  window._env_?.REACT_APP_SERVER_WS_URL ??
  process.env.REACT_APP_SERVER_WS_URL ??
  baseURL.replace("http", "ws") ??
  "ws://localhost:8000"

interface Workspace {
  id: string
}

type WebsocketChatProps = {
  workspace: Workspace
}

const WebsocketChat: React.FC<WebsocketChatProps> = ({ workspace }) => {
  const [chats, setChats] = useState<Chat[]>([])

  const socketUrl = `${socketURL}/ws/chat/${workspace.id}/`

  const { sendJsonMessage, lastMessage } = useWebSocket(socketUrl)

  useEffect(() => {
    if (lastMessage !== null)
      setChats(prev =>
        prev.concat({
          message: JSON.parse(lastMessage.data).message,
          sender: false,
        }),
      )
  }, [lastMessage, setChats])

  const handleInput = (message: string) => {
    sendJsonMessage({ message })
    setChats([...chats, { message, sender: true }])
  }

  return <ChatWindow chats={chats} onInput={handleInput} />
}

export default WebsocketChat
