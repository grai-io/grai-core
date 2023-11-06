import React from "react"
import { Box } from "@mui/material"
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
  <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
    <ChatHistory chats={chats} />
    <ChatInput onInput={onInput} />
  </Box>
)

export default ChatWindow
