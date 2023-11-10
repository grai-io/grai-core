import React, { useEffect } from "react"
import useChat from "helpers/useChat"
import ChatWindow from "./ChatWindow"

const WebsocketChat: React.FC = () => {
  const { messages, sendMessage, workspace, clearUnread } = useChat()

  const choices = messages.every(m => !m.sender)
    ? [
        "Is there a customer table in the prod namespace?",
        "Which tables have an email field?",
        "Produce a list of tables that aren't used by any application",
      ]
    : []

  useEffect(() => {
    clearUnread()
  }, [clearUnread])

  return (
    <ChatWindow
      messages={messages}
      choices={choices}
      onInput={sendMessage}
      workspaceId={workspace.id}
    />
  )
}

export default WebsocketChat
