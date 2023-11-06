import React from "react"
import { Box } from "@mui/material"
import ChatMessage, { GroupedChats } from "./ChatMessage"
import { Chat } from "./ChatWindow"

const combineChats = (chats: Chat[]) =>
  chats.reduce<GroupedChats[]>((acc, chat) => {
    const last = acc[acc.length - 1]
    if (last && last.sender === chat.sender) {
      last.messages.push(chat.message)
    } else {
      acc.push({ sender: chat.sender, messages: [chat.message] })
    }
    return acc
  }, [])

type ChatHistoryProps = {
  chats: Chat[]
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ chats }) => (
  <Box sx={{ flexGrow: 1, overflow: "auto", height: "200px" }}>
    {combineChats(chats).map((groupedChat, i) => (
      <ChatMessage key={i} groupedChat={groupedChat} />
    ))}
  </Box>
)

export default ChatHistory
