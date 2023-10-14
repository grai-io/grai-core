import { Card } from "@mui/material"
import React, { useState } from "react"
import ChatHistory from "./ChatHistory"
import ChatInput from "./ChatInput"

export type Chat = {
  message: string
  sender: boolean
}

const ChatWindow: React.FC = () => {
  const [chats, setChats] = useState<Chat[]>([])

  const handleInput = (message: string) => {
    setChats([...chats, { message, sender: true }])
  }

  return (
    <Card sx={{ mt: 3, p: 3 }}>
      <ChatHistory chats={chats} />
      <ChatInput onInput={handleInput} />
    </Card>
  )
}

export default ChatWindow
