import React from "react"
import { Box } from "@mui/material"
import ChatMessage, { GroupedChats } from "./ChatMessage"
import { Message } from "./ChatWindow"

const combineMessages = (messages: Message[]) =>
  messages.reduce<GroupedChats[]>((acc, chat) => {
    const last = acc[acc.length - 1]
    if (last && last.sender === chat.sender) {
      last.messages.push(chat.message)
    } else {
      acc.push({ sender: chat.sender, messages: [chat.message] })
    }
    return acc
  }, [])

type ChatHistoryProps = {
  messages: Message[]
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => (
  <Box sx={{ flexGrow: 1, overflow: "auto", height: "200px" }}>
    {combineMessages(messages).map((groupedChat, i) => (
      <ChatMessage key={i} groupedChat={groupedChat} />
    ))}
  </Box>
)

export default ChatHistory
