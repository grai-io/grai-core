import React from "react"
import { Box } from "@mui/material"
import ChatMessage from "./ChatMessage"
import { Chat } from "./ChatWindow"

type ChatHistoryProps = {
  chats: Chat[]
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ chats }) => (
  <Box sx={{ flexGrow: 1, overflow: "auto", height: "200px" }}>
    {chats.map((chat, i) => (
      <ChatMessage key={i} chat={chat} />
    ))}
  </Box>
)

export default ChatHistory
