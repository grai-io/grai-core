import React from "react"
import { Avatar, Box } from "@mui/material"
import ChatMessageComponent from "./ChatMessageComponent"

export type GroupedChats = {
  sender: boolean
  messages: string[]
}

type ChatMessageProps = {
  groupedChat: GroupedChats
}

const ChatMessage: React.FC<ChatMessageProps> = ({ groupedChat }) => {
  const sender = groupedChat.sender ? "user" : "agent"
  const messages = groupedChat.messages

  return (
    <Box sx={{ display: "flex", mb: 2, width: "100%"}}>
      {messages.map((msg, i) => (
        <Box key={i}>
          <ChatMessageComponent sender={sender} message={msg} />
        </Box>
      ))}
    </Box>
  )
}

export default ChatMessage
