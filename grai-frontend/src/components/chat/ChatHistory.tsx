import React from "react"
import { List, ListItem } from "@mui/material"
import { Chat } from "./ChatWindow"

type ChatHistoryProps = {
  chats: Chat[]
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ chats }) => (
  <List>
    {chats.map((chat, index) => (
      <ListItem
        key={index}
        disableGutters
        sx={{
          display: "flex",
          justifyContent: chat.sender ? null : "flex-end",
        }}
      >
        {chat.message}
      </ListItem>
    ))}
  </List>
)

export default ChatHistory
