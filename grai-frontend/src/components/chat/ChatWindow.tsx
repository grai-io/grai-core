import React from "react"
import { Card } from "@mui/material"
import ChatHistory from "./ChatHistory"
import ChatInput from "./ChatInput"

export type Chat = {
  message: string
  sender: boolean
}

type ChatWindowProps = {
  chats: Chat[]
  onInput: (message: string) => void
}

const ChatWindow: React.FC<ChatWindowProps> = ({ chats, onInput }) => (
  <Card sx={{ mt: 3, p: 3 }}>
    <ChatHistory chats={chats} />
    <ChatInput onInput={onInput} />
  </Card>
)

export default ChatWindow
