import React from "react"
import { Box } from "@mui/material"
import ChatHistory from "./ChatHistory"
import ChatInput from "./ChatInput"
import ResetChat from "./ResetChat"

export type Message = {
  message: string
  sender: boolean
}

type ChatWindowProps = {
  messages: Message[]
  choices: string[]
  onInput: (message: string) => void
  workspaceId: string
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  choices,
  onInput,
  workspaceId,
}) => (
  <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
    <ChatHistory messages={messages} choices={choices} onInput={onInput} />
    <ResetChat workspaceId={workspaceId} />
    <ChatInput onInput={onInput} />
  </Box>
)

export default ChatWindow
