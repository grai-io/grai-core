import React from "react"
import { Chat } from "./ChatWindow"
import { List, ListItem } from "@mui/material"

type ChatHistoryProps = {
  chats: Chat[]
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ chats }) => (
  <List>
    {chats.map((chat, index) => (
      <ListItem key={index} disableGutters>
        {chat.message}
      </ListItem>
    ))}
  </List>
)

export default ChatHistory
