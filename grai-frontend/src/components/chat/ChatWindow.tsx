import React from "react"
import { Box } from "@mui/material"
import ChatHistory from "./ChatHistory"
import ChatInput from "./ChatInput"
import ResetChat from "./ResetChat"

export type Chat = {
  message: string
  sender: boolean
}

type ChatWindowProps = {
  chats: Chat[]
  onInput: (message: string) => void
  workspaceId: string
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  chats,
  onInput,
  workspaceId,
}) => (
  <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
    <ChatHistory chats={chats} />
    <ResetChat workspaceId={workspaceId} />
    <ChatInput onInput={onInput} />
  </Box>
)

export default ChatWindow
